# core/crispy_patch.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Div

# ---- GLOBAL CONFIGURATION ----
DEFAULT_SUBMIT_TEXT = "Submit"
DEFAULT_FORM_METHOD = "post"
DEFAULT_FIELD_CLASS = "form-control"
COLUMNS_PER_ROW = 2
TEXTAREA_ROWS = 4        # default rows for Textarea fields
# -------------------------------

def add_bootstrap_classes(form_instance):
    """Add Bootstrap classes to all form fields"""
    for field_name, field in form_instance.fields.items():
        existing_class = field.widget.attrs.get("class", "")
        classes = f"{existing_class} {DEFAULT_FIELD_CLASS}".strip()
        field.widget.attrs["class"] = classes

def enhance_fields(form_instance):
    """Add extra polish to fields: textarea rows and placeholders"""
    for name, field in form_instance.fields.items():
        # Add placeholder from label or field name
        if not field.widget.attrs.get("placeholder"):
            field.widget.attrs["placeholder"] = field.label or name.replace("_", " ").title()
        
        # Make Textarea taller
        if isinstance(field.widget, forms.Textarea):
            field.widget.attrs.setdefault("rows", TEXTAREA_ROWS)

def add_crispy_helper(cls):
    """Automatically add FormHelper, submit button, Bootstrap classes, layout, and enhancements"""
    original_init = cls.__init__

    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        if not hasattr(self, 'helper'):
            self.helper = FormHelper()
            self.helper.form_method = DEFAULT_FORM_METHOD

            fields = list(self.fields.keys())
            if fields:
                layout_rows = []
                for i in range(0, len(fields), COLUMNS_PER_ROW):
                    chunk = fields[i:i+COLUMNS_PER_ROW]
                    columns = [Column(f, css_class=f'col-md-{12//COLUMNS_PER_ROW}') for f in chunk]

                    # Center last row if fewer fields
                    if len(chunk) < COLUMNS_PER_ROW:
                        offset = (COLUMNS_PER_ROW - len(chunk)) * (12 // (2 * COLUMNS_PER_ROW))
                        layout_rows.append(Row(Div(*columns, css_class=f'offset-md-{offset}')))
                    else:
                        layout_rows.append(Row(*columns))

                self.helper.layout = Layout(*layout_rows)

            if not any(isinstance(i, Submit) for i in self.helper.inputs):
                self.helper.add_input(Submit('submit', DEFAULT_SUBMIT_TEXT))

        add_bootstrap_classes(self)
        enhance_fields(self)

    cls.__init__ = __init__
    return cls

# Patch all forms globally
add_crispy_helper(forms.ModelForm)
add_crispy_helper(forms.Form)
