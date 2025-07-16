from mcp.server.fastmcp import FastMCP
import logging
import sys

# Set up logging to help debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("knowledge")



KNOWLEDGE_JSON = {
    "form": {
    "name": "form",
    "properties": [
      { "name": "formWidgets", "type": "object" },
      { "name": "dataoutput", "type": "object" },
      { "name": "dataset", "type": "object" },
      { "name": "message", "type": "string" },
      { "name": "name", "type": "string" },
      { "name": "show", "type": "boolean" }
    ],
    "methods": [
      { "name": "clearMessage", "syntax": "<Scope>.Widgets.<widgetName>.clearMessage()" },
      { "name": "highlightInvalidFields", "syntax": "<Scope>.Widgets.<widgetName>.highlightInvalidFields()" },
      { "name": "reset", "syntax": "<Scope>.Widgets.<widgetName>.reset()" },
      { "name": "submit", "syntax": "<Scope>.Widgets.<widgetName>.submit()" },
      { "name": "toggleMessage", "syntax": "<Scope>.Widgets.<widgetName>.toggleMessage(message)" }
    ],
    "events": [
      "<scope>.<widgetName>Beforesubmit = function ($event, widget, $data) {}; // Examples: Page.employeeFormBeforesubmit = function ($event, widget, $data) {//$data conatains input data of variable bound with form \n if (!$data.Employee.username || $data.Employee.username.length < 4) { Page.Actions.notifyError.invoke(); return false; } $data.Employee.createdOn = moment.now(); }; // Explanation: Triggers before form submit. Checks if 'username' is too short; if yes, shows error; else, sets createdOn.",
      "<scope>.<widgetName>Submit = function ($event, widget, $formData) {}; // Example: Partial.departmentFormSubmit = function ($event, widget, $formdata) {//$data conatains input data of variable bound with form \n console.log($formdata.Department.name}); }; // Explanation: Triggers on form submit and console logs department name.",
      "<scope>.<widgetName>Success = function ($event, widget, $data) {}; // Example: Page.employeeFormSuccess = function ($event, widget, $data) {//$data conatains dataSet of variable binded with form \n App.Variables.userDetails.dataSet = $data; Page.Widgets.employeeFirstname.caption = $data.firstname; }; // Explanation: On successful form submit, updates app variable and label caption.",
      "<scope>.<widgetName>Error = function ($event, widget, $data) {}; // Example: Page.employeeFormError = function ($event, widget, $data) {//$data conatains dataSet of variable binded with form \n console.log(\"Error from server:\", $data); }; // Explanation: Logs the error response if form submission fails."
    ]
  },
    "form-field": {
        "name" : "formfield",
        "properties": [
            {
                "name": "datavalue",
                "type": "string"
            },
            {
                "name": "inputtype",
                "type": "string"
            }
        ],
        "methods": [
            {
                "name": "setValidators",
                "syntax": "<Scope>.Widgets.<formName>.formWidgets.<fieldName>.setValidators([validators])",
                "examples": [{
                    "var VALIDATOR = App.getDependency('CONSTANTS').VALIDATOR; Page.Widgets.formName.formWidgets.fieldName.setValidators([{ type: VALIDATOR.REQUIRED, validator: true, // Display error message for the form field errorMessage: \"This field cannot be empty.\"}]);",
                    "Page.Widgets.tableName.columns.columnName.setValidators([lastNameVal]); function lastNameVal(field, table) { if (field.value && field.value.length < 2) //value key is used to access the value of field \n { return { errorMessage: \"Enter your full name.\" }; }}"
                },
          {
            "code": "Page.onReady = function() {\n  Page.Widgets.departmentForm.formfields.departmentName.setValidators([{\n    type: VALIDATOR.REQUIRED,\n    validator: true,\n    errorMessage: \"This field cannot be empty.\"\n  }]);\n};",
            "explanation": "On Page ready, sets a required validator on the field."
          },
          {
            "code": "Page.dialog1Opened = function ($event, widget) {\n  Page.Widgets.loginForm.formfields.username.setValidators([lastNameVal]);\n};\n\nfunction lastNameVal(field, form) {\n  if (field.value && field.value.length < 2) { //value key is used to access the value of field \n    return {\n      errorMessage: \"Enter your full name.\"\n    };\n  }\n}",
            "explanation": "Applies a custom validator on a form field."
          },
          {
            "code": "Page.Widgets.employeeForm.formfields.lastname.setValidators([\n  emailRequired,\n  {\n    type: VALIDATOR.REGEXP,\n    validator: /\\w+@\\w+\\.\\w{2,3}/,\n    errorMessage: \"Not a Valid Email\"\n  }\n]);\n\nfunction emailRequired(field, form) {\n  if (!field.value || field.value.length < 1) { //value key is used to access the value of field \n    return {\n      errorMessage: \"Email cannot be empty.\"\n    };\n  }\n}",
            "explanation": "Combines a custom required check and a regex email format validator."
          }
                ]
            },
            {
                "name": "setAsyncValidators",
                "syntax": "<Scope>.Widgets.<formName>.formWidgets.<fieldName>.setAsyncValidators([validators])",
                "examples": [
                    {"Page.Widgets.employeeInfoForm3.formWidgets.email.setAsyncValidators([emailAsync]); function emailAsync(field, form) { if (field.value) { return new Promise(function(resolve, reject) { var emailExists = Page.Variables.EmailData.dataSet.filter(function(data) { if (data.dataValue === field.value) { //value key is used to access the value of field \n return true; } }); if (emailExists.length != 0) { reject({ errorMessage: \"The email address is already registered.\" }); } resolve(); }); }}"},
                    {
            "code": "Page.Widgets.RegistationForm.formfields.email.setAsyncValidators([emailAsync]);\n\nfunction emailAsync(field, form) {\n  return new Promise(function(resolve, reject) {\n    if (field.value === \"duplicate@example.com\") { //value key is used to access the value of field \n      reject({\n        errorMessage: \"Email already exists.\"\n      });\n    } else {\n      resolve();\n    }\n  });\n}",
            "explanation": "Checks email uniqueness using async validator."
          }
                ]
            },
            {
                "name": "observeOn",
                "syntax": "<Scope>.Widgets.<formName>.formWidgets.<fieldName>.observeOn(fieldNamesArray)",
                "examples": [
                    {"Page.Widgets.EmployeeForm1.formWidgets.confirmpassword.setValidators([confirmPasswordEval]); Page.Widgets.EmployeeForm1.formWidgets.confirmpassword.observeOn(['password']); function confirmPasswordEval(field, form) { if (field.value && form.formWidgets.password.datavalue != field.value) { //value key is used to access the value of field return { errorMessage: \"Password & ConfirmPassword are not the same value\" }; } }"},
                    {
            "code": "Page.Widgets.EmployeeForm1.formfields.passowrd.setValidators([confirmPasswordEval]);\nPage.Widgets.EmployeeForm1.formfields.confirmpassword.observeOn(['password']);\n\nfunction confirmPasswordEval(field, form) {\n  if (field.value && form.formfields.password.value !== field.value) { //value key is used to access the value of field \n    return {\n      errorMessage: \"Password & Confirm Password are not the same value\"\n    };\n  }\n}",
            "explanation": "Adds confirm password logic to check matching values between password and confirm password."
          }
                ]
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "text": {
        "name" : "text",
        "properties": [
            {
                "name": "datavalue",
                "type": "string | number"
            },
            {
                "name": "displayformat",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "maxchars",
                "type": "number"
            },
            {
                "name": "placeholder",
                "type": "string"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "examples":[
            "let userInput = Page.Widgets.text1.datavalue;","Page.Widgets.text1.displayformat = '###-###';",
            "Page.Widgets.text1.disabled = true;","Page.Widgets.text1.maxchars = 100;","Page.Widgets.text1.show = false;"
        ]

        ,
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "select": {
        "name" : "select",
        "properties": [
            {
                "name": "datafield",
                "type": "string"
            },
            {
                "name": "dataset",
                "type": "Array<any>"
            },
            {
                "name": "datavalue",
                "type": "any"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "displayfield",
                "type": "string"
            },
            {
                "name": "placeholder",
                "type": "string"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "Examples":["let selectedCountry = Page.Widgets.selectCountry.datavalue;","Page.Widgets.selectCountry.disabled = true;","Page.Widgets.selectCountry.show = false;"],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "switch": {
        "name" : "switch",
        "properties": [
            {
                "name": "datafield",
                "type": "string"
            },
            {
                "name": "dataset",
                "type": "Array<any> | Object"
            },
            {
                "name": "datavalue",
                "type": "any"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "displayexpression",
                "type": "string"
            },
            {
                "name": "displayfield",
                "type": "string"
            },
            {
                "name": "orderby",
                "type": "string"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "fileupload": {
        "name" : "fileupload",
        "properties": [
            {
                "name": "uploadedFiles",
                "type": "array"
            },
            {
                "name": "selectedFiles",
                "type": "array"
            },
            {
                "name": "caption",
                "type": "string"
            },
            {
                "name": "contenttype",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "fileuploadmessage",
                "type": "string"
            },
            {
                "name": "maxfilesize",
                "type": "number"
            },
            {
                "name": "multiple",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Beforeselect = function ($event, widget, files) {};",
            "<scope>.<widgetName>Select = function ($event, widget, selectedFiles) {};",
            "<scope>.<widgetName>Error = function ($event, widget, files) {};"
        ]
    },
    "checkbox": {
        "name" : "checkbox",
        "properties": [
            {
                "name": "datavalue",
                "type": "boolean"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "checkboxset": {
        "name" : "checkboxset",
        "properties": [
            {
                "name": "dataset",
                "type": "array"
            },
            {
                "name": "displayvalue",
                "type": "string"
            },
            {
                "name": "datafield",
                "type": "string"
            },
            {
                "name": "datavalue",
                "type": "object"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "date": {
        "name" : "date",
        "properties": [
            {
                "name": "datavalue",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "datepattern",
                "type": "string"
            },
            {
                "name": "excludedays",
                "type": "string"
            },
            {
                "name": "excludedates",
                "type": "string"
            },
            {
                "name": "maxdate",
                "type": "string"
            },
            {
                "name": "mindate",
                "type": "string"
            }
        ]
    },
    "datetime": {
        "name" : "datetime",
        "properties": [
            {
                "name": "datavalue",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "datepattern",
                "type": "string"
            },
            {
                "name": "excludedays",
                "type": "string"
            },
            {
                "name": "excludedates",
                "type": "string"
            },
            {
                "name": "maxdate",
                "type": "string"
            },
            {
                "name": "mindate",
                "type": "string"
            }
        ]
    },
    "radioset": {
        "name" : "radioset",
        "properties": [
            {
                "name": "dataset",
                "type": "array"
            },
            {
                "name": "displayvalue",
                "type": "string"
            },
            {
                "name": "datafield",
                "type": "string"
            },
            {
                "name": "datavalue",
                "type": "object"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ]
    },
    "spinner": {
        "name" : "spinner",
        "properties": [
            {
                "name": "caption",
                "type": "string"
            },
            {
                "name": "image",
                "type": "string"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ]
    },
    "textarea": {
        "name" : "textarea",
        "properties": [
            {
                "name": "datavalue",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "maxchars",
                "type": "number"
            },
            {
                "name": "placeholder",
                "type": "string"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "number": {
        "name" : "number",
        "properties": [
            {
                "name": "datavalue",
                "type": "number"
            },
            {
                "name": "displayformat",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "maxchars",
                "type": "number"
            },
            {
                "name": "placeholder",
                "type": "string"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "chips": {
        "name" : "chips",
        "properties": [
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "readonly",
                "type": "string"
            },
            {
                "name": "dataset",
                "type": "array"
            },
            {
                "name": "displayvalue",
                "type": "string"
            },
            {
                "name": "datafield",
                "type": "string"
            },
            {
                "name": "datavalue",
                "type": "object"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};"
        ]
    },
    "search": {
        "name" : "search",
        "properties": [
            {
                "name": "datafield",
                "type": "string"
            },
            {
                "name": "dataset",
                "type": "Array<any>"
            },
            {
                "name": "datavalue",
                "type": "object"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "displayfield",
                "type": "string"
            },
            {
                "name": "placeholder",
                "type": "string"
            },
            {
                "name": "readonly",
                "type": "boolean"
            },
            {
                "name": "required",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newVal, oldVal) {};",
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Keypress = function ($event, widget) {};",
            "<scope>.<widgetName>clear = function ($event, widget) {};",
            "<scope>.<widgetName>Beforeservicecall = function (widget, inputData) {};",
            "<scope>.<widgetName>Datasetready = function (widget, data) {};",
            "<scope>.<widgetName>Submit = function ($event, widget) {};",
            "<scope>.<widgetName>Select = function ($event, widget, selectedValue) {};"
        ]
    },
    "button": {
        "name" : "button",
        "properties": [
            {
                "name": "caption",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": {
            "Web" : [
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Dbclick = function ($event, widget) {};",
            "<scope>.<widgetName>Mouseenter = function ($event, widget) {};",
            "<scope>.<widgetName>Mouseleave = function ($event, widget) {};"
            ],
            "Native_mobile" : [
            "<scope>.<widgetName>Tap = function ($event, widget) {};",
            "<scope>.<widgetName>Doubletap = function ($event, widget) {};",
            "<scope>.<widgetName>Longtap = function ($event, widget) {};",
            "<scope>.<widgetName>Touchstart = function ($event, widget) {};",
            "<scope>.<widgetName>Touchend = function ($event, widget) {};"
            ]
        }
    },
    "anchor": {
        "name" : "anchor",
        "properties": [
            {
                "name": "caption",
                "type": "string"
            },
            {
                "name": "hyperlink",
                "type": "string"
            },
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "target",
                "type": "string"
            }
        ],
        "events": [
            "<scope>.<widgetName>Focus = function ($event, widget) {};",
            "<scope>.<widgetName>Blur = function ($event, widget) {};",
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Dbclick = function ($event, widget) {};"
        ]
    },
    "designdialog": {
        "name" : "designdialog",
        "methods": [
            {
                "name": "close",
                "syntax": "<Scope>.Widgets.<widgetName>.close()"
            },
            {
                "name": "open",
                "syntax": "<Scope>.Widgets.<widgetName>.open()"
            }
        ],
        "events": [
            "<scope>.<widgetName>Opened = function ($event, widget) {};",
            "<scope>.<widgetName>Closed = function ($event, widget) {};"
        ]
    },
    "label": {
        "name" : "label",
        "properties": [
            {
                "name": "caption",
                "type": "string"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Dbclick = function ($event, widget) {};"
        ]
    },
    "list": {
        "name" : "list",
        "methods": [
            {
                "name": "clear",
                "syntax": "<Scope>.Widgets.<widgetName>.clear()"
            },
            {
                "name": "deselectItem",
                "syntax": "<Scope>.Widgets.<widgetName>.deselectItem(index)"
            },
            {
                "name": "getWidgets",
                "syntax": "<Scope>.Widgets.<widgetName>.getWidgets(widgetName, index)"
            }
        ],
        "properties": [
            {
                "name": "selecteditem",
                "type": "object",
                "Example":"Page.Widgets.listEmployees.selecteditem"
            },
            {
                "name": "selectedItemWidgets",
                "type": "object",
                "Example":"Page.Widgets.listEmployees.selectedItemWidgets"
            },
            {
                "name": "dataNavigator",
                "type": "boolean"
            },
            {
                "name": "dataset",
                "type": "Array<any>"
            },
            {
                "name": "navigation",
                "type": "boolean"
            },
            {
                "name": "pagesize",
                "type": "number"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
      "[Scope].[WidgetName]Click = function($event, widget) {}; // Example: Page.EmployeeListClick = function($event, widget) { const empId = widget.item.deptId; const deptName = widget.item.name; Page.Variables.getDepartmentDetails.setInput({ id: empId }); Page.Variables.getDepartmentDetails.invoke(); Page.Widgets.selectedDeptName.caption = `Selected: ${deptName}`; }; // Explanation: Uses widget.item for department data, fetches details, and updates a label.",
      "[Scope].[WidgetName]Dblclick = function($event, widget) {}; // Example: Page.EmployeeListDblclick = function($event, widget) { Page.Actions.goToPage_DeptDetails.invoke({ data: { deptId: widget.item.deptId, deptName: widget.item.name } }); }; // Explanation: Navigates to the department detail page with deptId and deptName.",
      "[Scope].[WidgetName]Mouseenter = function($event, widget) {}; // Example: Page.EmployeeListMouseenter = function($event, widget) { widget.itemClass += ' hover-highlight'; widget._currentItemWidgets.Name.caption = `Viewing: ${widget.item.name}`; }; // Explanation: Adds a hover class and updates a label.",
      "[Scope].[WidgetName]Mouseleave = function($event, widget) {}; // Example: Page.EmployeeListMouseleave = function($event, widget) { widget.itemClass = widget.itemClass.replace(' hover-highlight', ''); widget._currentItemWidgets.Name.caption = widget.item.name; }; // Explanation: Removes hover class and resets the label.",
      "[Scope].[WidgetName]Enterkeypress = function($event, widget, item, index) {}; // Example: Page.EmployeeListEnterkeypress = function($event, widget, item, index) { Page.Variables.searchUser.setInput({ keyword: item.name }); Page.Variables.searchUser.invoke(); }; // Explanation: Triggers a search when Enter is pressed.",
      "[Scope].[WidgetName]Paginationchange = function($event, widget, pageInfo) {}; // Example: Page.EmployeeListPaginationchange = function($event, widget, pageInfo) { console.log(\"Page changed to:\", pageInfo.page); Page.Variables.getPaginatedUsers.setInput({ page: pageInfo.page }); Page.Variables.getPaginatedUsers.invoke(); }; // Explanation: Triggers data reload when pagination changes.",
      "[Scope].[WidgetName]Render = function(widget, $data) {}; // Example: Page.EmployeeListRender = function(widget, $data) {//$data conatains dataSet of variable binded with list \n widget.selectItem(2); Page.Widgets.detailsCard.caption = `Selected: ${$data[2].name}`; }; // Explanation: Selects third item on render and updates a card."
    ]
    },
    "liItem": {
    "eventsDescription": "For any widget placed inside a List or Cards, all event handler signatures receive two additional parameters: `item` (the data object for this present li item or cards) and `currentItemWidgets` (current widget instances of all widgets present in list ). Use `item` to access present li item data, and `currentItemWidgets` to control or read values of current widgets at present li item.",
    "generalSyntax": "<scope>.<widgetName><Event> = function(Existing event parameters+ item, currentItemWidgets)",
    "parameters": {
      "item": "The data object for the current list/card item. For example: { id: 123, name: 'Alice', ... }",
      "currentItemWidgets": "Object mapping widget names to their widget instances inside the same list/card item. Use this to get or set properties on other widgets in this item."
    },
    "notes": [
      "All standard widget events (change, click, blur, focus, keypress, etc.) are supported using this extended signature inside List and Cards",
      "For List and Card, always use the extended signature with item and currentItemWidgets to react contextually to each row/card's data and UI."
    ],
    "examples": [
      {
       "standaloneWidgetSyntax": "Page.WmEnvironment_branchNameChange = function ($event, widget, newVal, oldVal) { ... }",
        "liItemWidgetSyntax": "Page.WmEnvironment_branchNameChange = function ($event, widget, item, currentItemWidgets, newVal, oldVal) { ... }"
      },
      {
        "standaloneWidgetSyntax": "Page.buttonLunchKeypress = function ($event, widget) { ... }",
        "liItemWidgetSyntax": "Page.buttonLunchKeypress = function ($event, widget, item, currentItemWidgets) { ... }"
      },
      {"standaloneWidgetSyntax": "Page.number1Change = function ($event, widget, newVal, oldVal) { ... }",
        "liItemWidgetSyntax": "Page.number1Change = function ($event, widget, item, currentItemWidgets, newVal, oldVal) { ... }"
        },
        {"standaloneWidgetSyntax": "Page.checkboxset1Change = function ($event, widget, newVal, oldVal) { ... }",
        "liItemWidgetSyntax": "Page.checkboxset1Change = function ($event, widget, item, currentItemWidgets, newVal, oldVal) { ... }"},
        { "standaloneWidgetSyntax": "Page.chips1Change = function ($event, widget, newVal, oldVal) { ... }",
        "liItemWidgetSyntax": "Page.chips1Change = function ($event, widget, item, currentItemWidgets, newVal, oldVal) { ... }"
        },
        {"standaloneWidgetSyntax": "Page.radioset2Change = function ($event, widget, newVal, oldVal) { ... }",
        "liItemWidgetSyntax": "Page.radioset2Change = function ($event, widget, item, currentItemWidgets, newVal, oldVal) { ... }"},
    
    ]
  },
    "chart": {
        "name" : "chart",
        "properties": [
            {
                "name": "title",
                "type": "string"
            },
            {
                "name": "disabled",
                "type": "boolean"
            },
            {
                "name": "type",
                "type": "string"
            },
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "showlabels",
                "type": "boolean"
            },
            {
                "name": "showlegend",
                "type": "boolean"
            }
        ]
    },
    "icon": {
        "name" : "icon",
        "properties": [
            {
                "name": "caption",
                "type": "string"
            },
            {
                "name": "iconclass",
                "type": "string"
            },
            {
                "name": "iconposition",
                "type": "string"
            },
            {
                "name": "iconurl",
                "type": "string"
            },
            {
                "name": "iconwidth",
                "type": "string"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ]
    },
    "picture": {
        "name" : "picture",
        "properties": [
            {
                "name": "picturesource",
                "type": "any"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Click = function ($event, widget) {};",
            "<scope>.<widgetName>Dbclick = function ($event, widget) {};"
        ]
    },
    "table": {
        "name" : "table",
        "methods": [
            {
                "name": "refreshData",
                "syntax": "<Scope>.Widgets.<widgetName>.refreshData()"
            },
            {
        "name": "setValidators",
        "syntax": "Page.Widgets.[tableWidgetName].columns.[columnName].setValidators([...])",
        "examples": [
          {
            "code": "Page.Widgets.environmentsTable.columns.isActive.setValidators([{\n  type: VALIDATOR.REQUIRED,\n  validator: true,\n  errorMessage: \"This field cannot be empty.\"\n}]);",
            "syntax": "Page.Widgets.[tableWidgetName].columns.[columnName].setValidators([...])",
            "explanation": "Sets a required validator on a table column."
          },
          {
            "code": "Page.Widgets.onBoardTable.columns.isBoarded.setValidators([lastNameVal]);\n\nfunction lastNameVal(field, table) {\n  if (field.value && field.value.length < 2) {\n    return {\n      errorMessage: \"Enter your full name.\"\n    };\n  }\n}",
            "explanation": "Applies a custom validator on a table column."
          }
        ]
      },
      {
        "name": "observeOn",
        "syntax": "Page.Widgets.[tableWidgetName].columns.[confirmColumn].observeOn(['password'])",
        "examples": [
          {
            "code": "Page.Widgets.staticVariable2Table1.columns.confirmpassword.observeOn(['password']);\n\nfunction confirmPasswordEval(field, table) {\n  if (field.value && table.columns.password.value !== field.value) {\n    return {\n      errorMessage: \"Password & Confirm Password are not the same value\"\n    };\n  }\n}",
            "explanation": "Validates that 'confirmPassword' matches 'password' in the specified table column context."
          }
        ]
      }
        ],
        "properties": [
            {
                "name": "title",
                "type": "string"
            },
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "selecteditem",
                "type": "object"
            }
        ],
        "events": [
      "[Scope].[TableName]Rowclick = function($event, widget, row) {}; // Example: Page.departmentTableRowclick = function($event, widget, row) { console.log(\"Clicked department row:\", row); Page.Variables.selectedDept.setData({ id: row.deptId, name: row.name, location: row.location }); Page.Widgets.label_deptName.caption = `Department: ${row.name}`; Page.Widgets.label_location.caption = `Location: ${row.location}`; Page.Widgets.label_budget.caption = `Budget: $${row.budget.toLocaleString()}`; Page.Actions.goToPage_DeptDetails.invoke({ data: { deptId: row.deptId, deptName: row.name } }); }; // Explanation: Uses row data to update labels, set a variable, and navigate to detail page.",
      "[Scope].[TableName]Select = function($event, widget, row) {}; // Example: Page.employeeTableSelect = function($event, widget, row) { console.log(\"Selected row data:\", row.index, row); }; // Explanation: Triggers when a row is selected.",
      "[Scope].[TableName]Deselect = function($event, widget, row) {}; // Example: Partial.employeeTableDeselect = function($event, widget, row) { console.log(\"Deselected row:\", row.index, row); }; // Explanation: Runs when a row is deselected.",
      "[Scope].[TableName]Headerclick = function($event, widget, column) {}; // Example: Page.employeeTableHeaderclick = function($event, widget, column) { console.log(\"Clicked header column:\", column.field); }; // Explanation: Triggers when a Data Table column header is clicked.",
      "[Scope].[TableName]Beforerowupdate = function($event, widget, row, options) {}; // Example: Page.employeeTableBeforerowupdate = function($event, widget, row, options) { if (row.status === '') { wmToaster.show('error', 'Status is required'); return false; } row.updatedAt = new Date(); }; // Explanation: Validates the 'status' field before row update and adds a timestamp.",
      "[Scope].[TableName]Rowupdate = function($event, widget, row) {}; // Example: Page.employeeTableRowupdate = function($event, widget, row) { console.log(\"Row updated successfully:\", row); }; // Explanation: Executes after a row update and logs the updated data.",
      "[Scope].[TableName]Beforerowinsert = function($event, widget, row, options) {}; // Example: Page.employeeTableBeforerowinsert = function($event, widget, row, options) { if (row.password.length < 6) { wmToaster.show('error', 'ERROR', 'Password too short'); return false; } row.createdAt = Date.now(); }; // Explanation: Validates password length before inserting a row.",
      "[Scope].[TableName]Rowinsert = function($event, widget, row) {}; // Example: Page.employeeTableRowinsert = function($event, widget, row) { console.log(\"New row added:\", row); }; // Explanation: Runs after inserting a new row, logging the inserted data.",
      "[Scope].[TableName]Beforerowdelete = function($event, widget, row, options) {}; // Example: Page.employeeTableBeforerowdelete = function($event, widget, row, options) { if (row.status === 'locked') { wmToaster.show('error', 'ERROR', 'Cannot delete locked row'); return false; } }; // Explanation: Prevents deletion if row has a 'locked' status.",
      "[Scope].[TableName]Rowdelete = function($event, widget, row) {}; // Example: Page.employeeTableRowdelete = function($event, widget, row) { console.log(\"Deleted row data:\", row); }; // Explanation: Fires after a row is deleted, logging the deleted data."
    ]
    },
    "video": {
        "name" : "video",
        "properties": [
            {
                "name": "mp4sourcepath",
                "type": "any"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ]
    },
    "tabs": {
        "name" : "tabs",
        "properties": [
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "methods": [
            {
                "name": "prev",
                "syntax": "<Scope>.Widgets.<widgetName>.prev()"
            },
            {
                "name": "next",
                "syntax": "<Scope>.Widgets.<widgetName>.next()"
            },
            {
                "name": "goToTab",
                "syntax": "<Scope>.Widgets.<widgetName>.goToTab(<tabIndex>)"
            },
            {
                "name": "getActiveTabIndex",
                "syntax": "<Scope>.Widgets.<widgetName>.getActiveTabIndex()"
            },
            {
                "name": "removePane",
                "syntax": "<Scope>.Widgets.<widgetName>.removePane(<tabPaneName>)"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newPaneIndex, oldPaneIndex) {};"
        ]
    },
    "tabPane": {
        "name" : "tabpane",
        "properties": [
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "isSelect",
                "type": "boolean"
            },
            {
                "name": "title",
                "type": "string"
            }
        ],
        "methods": [
            {
                "name": "select",
                "syntax": "<Scope>.Widgets.<widgetName>.select()"
            },
            {
                "name": "deselect",
                "syntax": "<Scope>.Widgets.<widgetName>.deselect()"
            },
            {
                "name": "remove",
                "syntax": "<Scope>.Widgets.<widgetName>.remove()"
            }
        ],
        "events": [
            "<scope>.<widgetName>Load = function ($event, widget) {};",
            "<scope>.<widgetName>Select = function ($event, widget) {};"
        ]
    },
    "wizard": {
        "name" : "wizard",
        "properties": [
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "cancelable",
                "type": "boolean"
            },
            {
                "name": "enableNext",
                "type": "boolean"
            }
        ],
        "methods": [
            {
                "name": "cancel",
                "syntax": "<Scope>.Widgets.<widgetName>.cancel()"
            },
            {
                "name": "done",
                "syntax": "<Scope>.Widgets.<widgetName>.done()"
            },
            {
                "name": "next",
                "syntax": "<Scope>.Widgets.<widgetName>.next()"
            },
            {
                "name": "prev",
                "syntax": "<Scope>.Widgets.<widgetName>.prev()"
            },
            {
                "name": "skip",
                "syntax": "<Scope>.Widgets.<widgetName>.skip()"
            }
        ],
        "events": [
            "<scope>.<widgetName>Cancel = function (widget, steps) {};",
            "<scope>.<widgetName>Done = function (widget, steps) {};"
        ]
    },
    "wizardstep": {
        "name" : "wizardstep",
        "properties": [
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "enableSkip",
                "type": "boolean"
            },
            {
                "name": "title",
                "type": "string"
            }
        ],
        "events": [
            "<scope>.<widgetName>Next = function (widget, currentStep, stepIndex) {};",
            "<scope>.<widgetName>Prev = function (widget, currentStep, stepIndex) {};",
            "<scope>.<widgetName>Skip = function (widget, currentStep, stepIndex) {};"
        ]
    },
    "accordion": {
        "name" : "accordion",
        "properties": [
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "methods": [
            {
                "name": "removePane",
                "syntax": "<Scope>.Widgets.<widgetName>.removePane()"
            },
            {
                "name": "expandPane",
                "syntax": "<Scope>.Widgets.<widgetName>.expandPane(index)"
            },
            {
                "name": "addPane",
                "syntax": "<Scope>.Widgets.<widgetName>.addPane(pane)"
            }
        ],
        "events": [
            "<scope>.<widgetName>Change = function ($event, widget, newPaneIndex, oldPaneIndex) {};"
        ]
    },
    "accordionpane": {
        "name" : "accordionpane",
        "properties": [
            {
                "name": "show",
                "type": "boolean"
            },
            {
                "name": "content",
                "type": "string"
            },
            {
                "name": "title",
                "type": "string"
            }
        ],
        "methods": [
            {
                "name": "expand",
                "syntax": "<Scope>.Widgets.<widgetName>.expand()"
            },
            {
                "name": "collapse",
                "syntax": "<Scope>.Widgets.<widgetName>.collapse()"
            },
            {
                "name": "toggle",
                "syntax": "<Scope>.Widgets.<widgetName>.toggle()"
            },
            {
                "name": "remove",
                "syntax": "<Scope>.Widgets.<widgetName>.remove()"
            }
        ],
        "events": [
            "<scope>.<widgetName>Expand = function ($event, widget) {};",
            "<scope>.<widgetName>Collapse = function ($event, widget) {};"
        ]
    },
    "breadcrumb": {
        "name" : "breadcrumb",
        "properties": [
            {
                "name": "dataset",
                "type": "Array"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ]
    },
    "popover": {
        "name" : "popover",
        "properties": [
            {
                "name": "content",
                "type": "any"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "methods": [
            {
                "name": "open",
                "syntax": "<Scope>.Widgets.<widgetName>.open()"
            },
            {
                "name": "close",
                "syntax": "<Scope>.Widgets.<widgetName>.close()"
            }
        ],
        "events": [
            "<scope>.<widgetName>Show = function ($event, widget) {};",
            "<scope>.<widgetName>Hide = function ($event, widget) {};"
        ]
    },
    "menu": {
        "name" : "menu",
        "properties": [
            {
                "name": "dataset",
                "type": "Array"
            },
            {
                "name": "datavalue",
                "type": "string"
            },
            {
                "name": "show",
                "type": "boolean"
            }
        ],
        "events": [
            "<scope>.<widgetName>Show = function ($event, widget, $item) {};"
        ]
    },
    "wm.LiveVariable": {
        "name" : "wm.LiveVariable",
        "properties": [
            {
                "name": "dataSet",
                "type": "object"
            }
        ],
        "methods": [
            {
                "name": "listRecords",
                "syntax": "<scope>.Variables.<crudVariableName>.listRecords();"
            },
            {
                "name": "createRecord",
                "syntax": "<scope>.Variables.<crudVariableName>.createRecord({ \"row\" :entityJsonObject});"
            },
            {
                "name": "deleteRecord",
                "syntax": "<scope>.Variables.<crudVariableName>.deleteRecord({ \"row\" :entityJsonObjectWithPrimaryKeyField});"
            },
            {
                "name": "updateRecord",
                "syntax": "<scope>.Variables.<crudVariableName>.updateRecord({ \"row\" :entityJsonObject});"
            },
            {
                "name": "invoke",
                "syntax": "<scope>.Variables.<crudVariableName>.invoke();",
                "examples": [
        {
          "syntax": "[Scope].Variables.[variableName].setInput({ key: value });\n[Scope].Variables.[variableName].invoke();",
          "code": "Page.Variables.getDepartmentDetails.setInput({ id: empId });\nPage.Variables.getDepartmentDetails.invoke();",
          "explanation": "Sets input parameters using `setInput()` and invokes the variable to fetch data or perform an operation."
        },
        {
          "syntax": "[Scope].Variables.[VariableName].invoke({ inputFields }, successCallback, errorCallback);",
          "code": "App.Variables.wsGetCoreProjects.invoke({\n  inputFields: {\n    platformType: widget.item.platformType.toUpperCase() === 'MOBILE' ? 'NATIVE_MOBILE' : widget.item.platformType.toUpperCase(),\n    projectType: 'APPLICATION'\n  }\n}, function(data) {\n  enableCustomization(data);\n}, function(error) {\n  console.log(\"Error:\", error);\n});",
          "explanation": "Invoke the variable with input fields and handle success/error inline for this call only."
        }
      ]
            },
            {
                "name": "setInput",
                "syntax": "<scope>.Variables.<crudVariableName>.setInput(<key1>, <value1>)",
                "examples": [
        {
          "code": "var sv = Page.Variables.[variable_name];\nsv.setInput(\"fname\", \"Peter\");\nsv.setInput(\"lname\", \"Parker\");\nsv.invoke();",
          "explanation": "Set input fields individually before invoking."
        },
        ]
            },
            {
                "name": "setInput",
                "syntax": "<scope>.Variables.<crudVariableName>.setInput({ <key1>: <value1>, <key2>: <value2> })",
                "examples":[{
          "code": "var sv = Page.Variables.[variable_name];\nsv.setInput({\n  fname: \"Peter\",\n  lname: \"Parker\"\n});\nsv.invoke();",
          "explanation": "Set multiple inputs in a single object before invoking."
        }]
            }
        ],
        "events": [
    "<scope>.<variableName>onBeforeDatasetReady = function (variable, data) {}; // Example: Page.dbGetEmployeeonBeforeDatasetReady = function (variable, data) { data.forEach((item) => { item.studioProjectUrl = App.getStudioPath(item); }); return data; }; // Explanation: Runs before dataset is bound to the UI. Modifies each record by adding a computed URL using an App function.",
    "<scope>.<variableName>onResult = function (variable, data) {}; // Example: Page.dbGetEmployeeonResult = function (variable, data) { console.log(\"onResult triggered:\", data); Page.Variables.filteredData.dataSet = data.filter(app => app.isActive); }; // Explanation: Filters only active entries and saves them to another variable.",
    "<scope>.<variableName>onSuccess = function (variable, data) {}; // Example: Page.wsGetCoreProjectsonSuccess = function(variable, data) { console.log(\"Success handler triggered:\", data); }; // Explanation: Registers a permanent event handler for success.",
    "<scope>.<variableName>onError = function (variable, data) {}; // Example: Page.jsCreateEmployeeonError = function (variable, data) { console.error(\"onError triggered:\", data); Page.Variables.hasError.dataSet = true; }; // Explanation: Logs the error and flags a variable on failure.",
    "<scope>.<variableName>onBeforeInsertRecord = function (variable, inputData, options) {};",
    "<scope>.<variableName>onBeforeListRecords = function (variable, dataFilter, options) {};",
    "<scope>.<variableName>onCanUpdate = function (variable, data) {}; // Example: Page.jvInvokeServiceonCanUpdate = function (variable, inputData) { if (!inputData || !inputData.appName) { console.warn(\"Update blocked: Missing appName\"); return false; } return true; }; // Explanation: Prevents update call when 'appName' is missing in input."
  ]
    },
    "wm.ServiceVariable": {
        "name" : "wm.ServiceVariable",
        "properties": [
            {
                "name": "dataSet",
                "type": "object"
            }
        ],
        "methods": [
            {
                "name": "invoke",
                "syntax": "<scope>.Variables.<ServiceVariableName>.invoke();",
                "parameters": [
                    {
                        "name": "options",
                        "type": "key value pairs",
                        "description": " It can have fields as inputFields (key-value pair of inputData), page (pagination for Query Service Variable), size (pagination for Query Service Variable), orderBy (pagination for Query Service Variable)"
                    },
                    {
                        "type": "successCallback",
                        "description": "an optional callback method called on successful invocation of the variable."
                    },
                    {
                        "type": "errorCallback",
                        "description": "an optional callback method called on error invocation of the variable."
                    }
                ],
                 "examples": [
        {
          "syntax": "[Scope].Variables.[variableName].setInput({ key: value });\n[Scope].Variables.[variableName].invoke();",
          "code": "Page.Variables.getDepartmentDetails.setInput({ id: empId });\nPage.Variables.getDepartmentDetails.invoke();",
          "explanation": "Sets input parameters using `setInput()` and invokes the variable."
        },
        {
          "syntax": "var sv = [Scope].Variables.[variableName];\nsv.invoke({ inputFields }, successCallback, errorCallback);",
          "code": "var sv = Page.Variables.[variable_name];\nsv.invoke({ inputFields: { fname: \"Steve\", lname: \"Rogers\" } }, function(data) { console.log(\"success\", data); }, function(error) { console.log(\"error\", error); });",
          "explanation": "Invoke with dynamic data, success, and error callbacks."
        }
      ]
            },
            {
                "name": "cancel",
                "syntax": "<scope>.Variables.<serviceVariableName>.cancel()"
            },
            {
      "name": "setInput",
      "syntax": "<scope>.Variables.<serviceVariableName>.setInput(<key1>, <value1>)",
      "examples": [
        {
          "syntax": "var sv = [Scope].Variables.[variableName];\nsv.setInput('key', value);\nsv.invoke();",
          "code": "var sv = Page.Variables.[variable_name];\nsv.setInput(\"fname\", \"Peter\");\nsv.setInput(\"lname\", \"Parker\");\nsv.invoke();",
          "explanation": "Set input fields individually before invoking."
        },
        {
          "syntax": "var sv = [Scope].Variables.[variableName];\nsv.setInput({ key1: value1, key2: value2 });\nsv.invoke();",
          "code": "var sv = Page.Variables.[variable_name];\nsv.setInput({ fname: \"Peter\", lname: \"Parker\" });\nsv.invoke();",
          "explanation": "Set multiple inputs in a single object before invoking."
        }
      ]
    },
            {
                "name": "clearData",
                "syntax": "<scope>.Variables.<serviceVariableName>.clearData()"
            },
            {
                "name": "getData",
                "syntax": "<scope>.Variables.<serviceVariableName>.getData()"
            }
        ],
        "events": [
    "<scope>.<variableName>onBeforeDatasetReady = function (variable, data) {}; // Example: Page.dbGetEmployeeonBeforeDatasetReady = function (variable, data) { data.forEach((item) => { item.studioProjectUrl = App.getStudioPath(item); }); return data; }; // Explanation: Runs before dataset is bound to the UI.",
    "<scope>.<variableName>onResult = function (variable, data) {}; // Example: Page.dbGetEmployeeonResult = function (variable, data) { console.log(\"onResult triggered:\", data); Page.Variables.filteredData.dataSet = data.filter(app => app.isActive); }; // Explanation: Filters and sets data.",
    "<scope>.<variableName>onSuccess = function (variable, data) {}; // Example: Page.wsGetCoreProjectsonSuccess = function(variable, data) { console.log(\"Success handler triggered:\", data); }; // Explanation: Registers a permanent event handler for success.",
    "<scope>.<variableName>onError = function (variable, data) {}; // Example: Page.jsCreateEmployeeonError = function (variable, data) { console.error(\"onError triggered:\", data); Page.Variables.hasError.dataSet = true; }; // Explanation: Logs the error and flags a variable on failure.",
    "<scope>.<variableName>onBeforeUpdate = function (variable, inputData) {}; // Example: Page.mdToggleDataonBeforeUpdate = function (variable, inputData) { inputData.lastModified = moment().format(); inputData.updatedBy = App.Variables.currentUser.dataSet.username; }; // Explanation: Adds metadata before update.",
    "<scope>.<variableName>onCanUpdate = function (variable, data) {}; // Example: Page.jvInvokeServiceonCanUpdate = function (variable, inputData) { if (!inputData || !inputData.appName) { console.warn(\"Update blocked: Missing appName\"); return false; } return true; }; // Explanation: Prevents update call when 'appName' is missing in input."
  ]
    },
    "wm.Variable": {
        "name" : "wm.Variable",
        "properties": [
            {
                "name": "dataSet",
                "type": "any"
            },
            {
                "name": "type",
                "type": "string"
            }
        ],
        "methods": [
            {
                "name": "setValue",
                "syntax": "<scope>.Variables.<serviceVariableName>.setValue(<key1>, <value1>)"
            },
            {
                "name": "setData",
                "syntax": "<scope>.Variables.<serviceVariableName>.setData({ <key1>: <value1>, <key2>: <value2> })"
            }
        ]
    },
    "wm.NavigationVariable": {
        "name" : "wm.NavigationVariable",
        "methods": [
    {
      "name": "invoke",
      "syntax": "<Scope>.Actions.<navigationActionName>.invoke();",
      "examples": [
        {
          "syntax": "[Scope].Actions.goToPage_<PageName>.invoke();",
          "code": "Page.Actions.goToPage_TestPage.invoke();",
          "explanation": "Triggers navigation to 'TestPage' without passing any parameters."
        },
        {
          "syntax": "[Scope].Actions.goToPage_<PageName>.invoke({ data: { key1: value1, key2: value2 } });",
          "code": "Page.Actions.goToPage_EmployeeDetailsPage.invoke({ data: { 'paramDept': '1', 'paramEmpdId': '2' } });",
          "explanation": "Navigates to 'EmployeeDetailsPage' and passes parameters."
        }
      ]
    },
    {
      "name": "setData",
      "syntax": "<Scope>.Actions.<navigationActionName>.setData({ 'param1': \"param value\",\"param2\": \"param value 2\" })",
      "examples": [
        {
          "syntax": "[Scope].Actions.goToPage_<PageName>.nv.setData({ key: value }); nv.invoke();",
          "code": "var nv = Partial.Actions.goToPage_TestPage;\nnv.setData({ 'param1': 'param value', 'param2': 'param value 2' });\nnv.invoke();",
          "explanation": "Uses setData to pass values before invoking navigation."
        }
      ]
    }
  ]
    },
    "wm.NotificationVariable": {
        "name" : "wm.NotificationVariable",
        "properties": [],
        "methods": [
        {
        "name": "invoke",
        "syntax": "<Scope>.Actions.<notificationActionName>.invoke();",
        "examples": [
            {
            "syntax": "[Scope].Actions.<NotificationActionName>.invoke();",
            "code": "Page.Actions.notificationAction1.invoke();",
            "explanation": "Triggers the default notification action."
            },
            {
            "syntax": "[Scope].Actions.<NotificationActionName>.invoke({ message: 'text', position: 'bottom right', class: 'info' });",
            "code": "Partial.Actions.notificationAction1.invoke({ message: 'My custom message', position: 'bottom right', class: 'info' });",
            "explanation": "Displays a custom toast notification."
            },
            {
            "syntax": "[Scope].Actions.<NotificationActionName>.invoke({ data: { key: value } });",
            "code": "Page.Actions.notificationAction1.invoke({ data: { mode: 'edit' } });",
            "explanation": "Triggers a notification and sends a data object."
            }
        ]
        },
        {
      "name": "setData",
      "syntax": "<Scope>.Actions.<navigationActionName>.setData({ 'param1': \"param value\",\"param2\": \"param value 2\" })"
    },
        ]
    },
    "wm.DeviceVariable": {
        "name" : "wm.DeviceVariable",
        "properties": [{"name": "dataSet","type": "any"}],
        "methods": [{
            "name": "invoke",
            "syntax": "<scope>.Variables.<DeviceVariableName>.invoke();",
            "parameters": [
                {
                    "name": "options",
                    "type": "key value pairs",
                    "description": " It can have fields as inputFields (key-value pair of inputData), page (pagination for Query Service Variable), size (pagination for Query Service Variable), orderBy (pagination for Query Service Variable)"
                },
                {
                    "type": "successCallback",
                    "description": "an optional callback method called on successful invocation of the variable."
                },
                {
                    "type": "errorCallback",
                    "description": "an optional callback method called on error invocation of the variable."
                }
            ]
        }]
    }
}

@mcp.tool()
async def get_knowledge(keys: list[str]) -> str:
    """
    Pass list of widget types or variable categories to retrieve knowledge for.
    keys: List of widget or variable categories to retrieve knowledge for.
    Returns: str: The combined knowledge for the given keys in JSON format.
    """
    logger.info(f"Getting knowledge for: {keys}")
    result = ""

    for k in keys:
        result += str(KNOWLEDGE_JSON[k]) + "\n"

    return result

if __name__ == "__main__":
    try:
        logger.info("Starting mcp-server-demo MCP server...")
        logger.info(f"Python version: {sys.version}")
        logger.info("Server initialized, waiting for connections...")
        
        # Initialize and run the server
        mcp.run(transport="sse")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        raise