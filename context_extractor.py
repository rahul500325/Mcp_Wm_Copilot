import requests
import json
from urllib.parse import unquote_plus
from bs4 import BeautifulSoup

# You may want to set this globally or pass as a parameter
origin = "https://www.wavemakeronline.com"  # <-- Set this appropriately

def get_api_response(url, auth_cookie):
    try:
        print(url)
        headers = {
            "Cookie" :
                f'auth_cookie = {auth_cookie}'
        }
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        print(response)
        return response.json()
    except Exception:
        return None

def get_project_metadata(project_id, auth_cookie):
    details_url = f"{origin}/studio/services/projects/{project_id}/details"
    project_details = get_api_response(details_url, auth_cookie)
    if not project_details:
        return {}
    return {
        "projectName": project_details.get("displayName"),
        "projectType": project_details.get("platformType")
    }

def get_prefabs_data(project_id, page_name, auth_cookie):
    prefabs_data_url = f"{origin}/studio/services/projects/{project_id}/pages/{page_name}/prefabs-data"
    prefabs_data = get_api_response(prefabs_data_url, auth_cookie)
    prefabs_list = []
    if not prefabs_data:
        return prefabs_list
    for prefab, data in prefabs_data.items():
        curr_prefab = {"name": prefab}
        config = data.get('config', {})
        curr_prefab["properties"] = config.get("properties")
        curr_prefab["methods"] = config.get("methods")
        events = config.get("events", {})
        events["onLoad"] = {"description": "triggers on load of prefab"}
        events["onDestroy"] = {"description": "triggers on destroy of prefab"}
        curr_prefab["events"] = events
        prefabs_list.append(curr_prefab)
    return prefabs_list

def decode_variables(encoded_string):
    decoded = unquote_plus(encoded_string)
    return json.loads(decoded)

def get_partial_data(project_id, partial_name, auth_cookie):
    partial_name = partial_name.strip()
    partial_url = f"{origin}/studio/services/projects/{project_id}/pages/{partial_name}/page.min.json"
    partial_data = get_api_response(partial_url, auth_cookie)
    if not partial_data:
        return {}
    partial_widgets = extract_widgets_preserving_children(partial_data["markup"], project_id)
    variables, actions = get_variables(decode_variables(partial_data["variables"]), project_id)
    return {
        "Widgets": partial_widgets,
        "Variables": variables,
        "Actions": actions
    }

def get_variables(variables_json, project_id, auth_cookie):
    action_categories = {"NavigationVariable", "NotificationVariable", "LogoutVariable", "LoginVariable", "TimerVariable"}
    variables = {}
    actions = {}

    for name, details in variables_json.items():
        category = details.get("category", "").replace("wm.", "")
        is_action = category in action_categories
        filtered = {}

        if category == "Variable":
            filtered["type"] = details.get("type")
            filtered["dataSet"] = details.get("dataSet")
        elif is_action:
            if category == "NavigationVariable":
                operation = details.get("operation", "")
                page_name = details.get("pageName")
                filtered["target_location"] = f"{operation} {page_name}" if page_name else operation
            elif category == "NotificationVariable":
                filtered["type"] = details.get("operation")
            elif category == "TimerVariable" and details.get("delay"):
                filtered["delay"] = details["delay"]
        elif details.get("service") and details.get("operationId"):
            service = details["service"]
            operation_id = details["operationId"]
            service_defs_url = f"{origin}/studio/services/projects/{project_id}/resources/content/project/services/{service}/src/servicedefs/{service}-service-definitions.json"
            service_defs = get_api_response(service_defs_url, auth_cookie)
            parameters = []
            if service_defs and operation_id in service_defs:
                parameters_set = service_defs[operation_id]["wmServiceOperationInfo"]["parameters"]
                for parameter in parameters_set:
                    obj = {"name": parameter["name"]}
                    obj["type"] = parameter.get("parameterType", parameter.get("type"))
                    for binding in details.get("dataBinding", []):
                        if binding.get("target") == parameter["name"]:
                            obj["value"] = binding.get("value")
                    parameters.append(obj)
            types_url = f"{origin}/studio/services/projects/{project_id}/services/{service}/types"
            types = get_api_response(types_url, auth_cookie)
            data_set = []
            if types and "types" in types and details.get("type") in types["types"]:
                fields = types["types"][details["type"]].get("fields", {})
                for field_name, field_info in fields.items():
                    data_set.append({"name": field_name, "type": field_info.get("type")})
            else:
                data_set.append("value")
            filtered["parameters"] = parameters
            filtered["dataSet"] = data_set
        elif category == "LiveVariable":
            columns = details.get("propertiesMap", {}).get("columns", [])
            filtered["dataSet"] = [data.get("fieldName") for data in columns]
        elif category == "DeviceVariable":
            filtered["operation"] = details.get("operation")

        filtered["category"] = details.get("category")
        if not is_action:
            variables[name] = filtered
        else:
            actions[name] = filtered
    return variables, actions

def extract_widgets_preserving_children(encoded_markup, project_id, auth_cookie):
    decoded_str = unquote_plus(encoded_markup.replace("+", " "))
    soup = BeautifulSoup(decoded_str, "html.parser")
    tag_data = {}

    DEFAULT_WIDGETS = [
        "wm-page", "wm-header", "wm-top-nav", "wm-content", "wm-left-panel",
        "wm-page-content", "wm-composite", "wm-footer", "wm-gridrow",
        "wm-gridcolumn", "wm-layoutgrid", "wm-listtemplate", "wm-partial", "wm-dialogactions",
        "wm-card", "wm-listtemplate", "wm-livetable", "html", "head", "body", "wm-prefab-container"
    ]
    PARTIAL_WIDGETS = ["wm-container", "wm-panel", "accordionpane", "wm-tabpane", "wm-card-content", "wm-wizardstep"]
    DATA_WIDGETS = ["wm-list", "wm-card", "wm-table", "wm-form", "wm-liveform"]
    CHILD_WIDGETS = ["wm-form-field", "wm-table-column", "wm-param"]
    list_item_widgets = []

    tags = soup.find_all(True)
    global PageType
    PageType = None
    if tags and len(tags) > 3:
        tag_name = tags[3].name.lower()
        if tag_name == "wm-page":
            PageType = "Page"
        elif tag_name == "wm-partial":
            PageType = "Partial"
        elif tag_name == "wm-prefab-container":
            PageType = "Prefab"
        else:
            PageType = "Page"

    for tag in tags:
        tag_name_lower = tag.name.lower()
        if tag_name_lower in DEFAULT_WIDGETS or tag_name_lower in CHILD_WIDGETS or tag.get("name") in list_item_widgets:
            continue
        tag_name = tag_name_lower.replace("wm-", "")
        name = tag.get("name")
        if not name:
            continue
        tag_info = {"category": tag_name}
        if tag.has_attr("dataset"):
            tag_info["dataset"] = tag["dataset"]
        if tag.has_attr("caption"):
            tag_info["caption"] = tag["caption"]
        if tag.has_attr("datafield"):
            tag_info["datafield"] = tag["datafield"]
        if tag.has_attr("type"):
            tag_info["type"] = tag["type"]
        if tag.has_attr("iconclass"):
            tag_info["iconclass"] = tag["iconclass"]
        for attr, value in tag.attrs.items():
            if attr.startswith("on-"):
                tag_info[attr] = value

        if tag_name_lower in PARTIAL_WIDGETS and tag.has_attr("content"):
            params = []
            for child in tag.find_all(True):
                if child.name.lower() == "wm-param":
                    param = {"name": child.get("name"), "type": child.get("type")}
                    params.append(param)
            partial_name = tag["content"]
            tag_info["type"] = "partial"
            tag_info["partialParams"] = params
            tag_info["content"] = partial_name
            partialdata = get_partial_data(project_id, partial_name, auth_cookie)
            tag_info["Widgets"] = partialdata.get("Widgets")
            tag_info["Variables"] = partialdata.get("Variables")
            tag_info["Actions"] = partialdata.get("Actions")
        elif tag_name_lower == "wm-container":
            continue

        if tag_name_lower in DATA_WIDGETS:
            children = {}
            for child in tag.find_all(True):
                child_tag = child.name.lower()
                if not (child.has_attr("name") or child.has_attr("caption")):
                    continue
                child_name = child.get("name") or child.get("caption")
                if not child_name or child_tag in DEFAULT_WIDGETS:
                    continue
                childtagname = child_tag.replace("wm-", "")
                child_widget = {"category": childtagname}
                if child.has_attr("caption"):
                    child_widget["caption"] = child["caption"]
                if child.has_attr("widget"):
                    child_widget["widget"] = child["widget"]
                elif child.has_attr("type"):
                    child_widget["type"] = child["type"]

                if tag_name_lower in ["wm-form", "wm-liveform"]:
                    children[child_name] = child_widget
                elif tag_name_lower == "wm-table":
                    if child_tag == "wm-table-column":
                        children[child_name] = child_widget
                else:
                    list_item_widgets.append(child_name)
                    children[child_name] = child_widget

            if children:
                if tag_name_lower in ["wm-form", "wm-liveform"]:
                    tag_info["formWidgets"] = children
                elif tag_name_lower == "wm-list":
                    tag_info["list-item-widgets"] = children
                elif tag_name_lower == "wm-table":
                    tag_info["table-columns"] = children
                else:
                    tag_info["children"] = children
        tag_data[name] = tag_info
    return tag_data

def get_app_context(project_id, page_name, auth_cookie):
    project_id = project_id.strip()
    page_name = page_name.strip()
    global PageType
    PageType = ""
    page_data_url = f"{origin}/studio/services/projects/{project_id}/pages/{page_name}/page.min.json"
    page_data = get_api_response(page_data_url, auth_cookie)
    if not page_data:
        return {"appContext": {}, "projectName": "null"}
    widgets = extract_widgets_preserving_children(page_data["markup"], project_id, auth_cookie)
    variables, actions = get_variables(decode_variables(page_data["variables"]), project_id, auth_cookie)
    app_context = {
        PageType: {
            "Widgets": widgets,
            "Variables": variables,
            "Actions": actions
        }
    }
    if PageType != "Prefab":
        common_page_url = f"{origin}/studio/services/projects/{project_id}/pages/Common/page.min.json"
        app_variables_url = f"{origin}/studio/services/projects/{project_id}/variables"
        app_data = get_api_response(common_page_url, auth_cookie)
        if app_data:
            common_widgets = extract_widgets_preserving_children(app_data["markup"], project_id, auth_cookie)
            app_variables = get_api_response(app_variables_url, auth_cookie)
            if app_variables and common_widgets:
                app_vars, app_acts = get_variables(app_variables, project_id, auth_cookie)
                app_context["App"] = {
                    "Widgets": common_widgets,
                    "Variables": app_vars,
                    "Actions": app_acts
                }
    else:
        config_url = f"{origin}/studio/services/projects/{project_id}/resources/content/web/config.json"
        configuration = get_api_response(config_url, auth_cookie)
        app_context["configuration"] = {
            "Properties": configuration.get("properties"),
            "Methods": configuration.get("methods"),
            "Events": configuration.get("events")
        }
    project_details = get_project_metadata(project_id, auth_cookie)
    project_details["pageName"] = page_name
    project_details["pageType"] = PageType
    app_context["metaData"] = project_details
    prefabs = get_prefabs_data(project_id, page_name, auth_cookie)
    if prefabs:
        app_context["prefabs"] = prefabs
    return {"appContext": app_context, "projectDetails": project_details}

def build_llm_context(project_id, page_name, auth_cookie):
    return json.dumps(get_app_context(project_id, page_name, auth_cookie))  # <-- serialize to JSON

# For pretty printing in the console:
print(build_llm_context("WMPRJ2c91808897762f7b0197870358240282", "Main", "0yvzDZsLn2P6SWBqd7v6Z5s7e16ab8ece34d9"))
