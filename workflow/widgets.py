from urllib.parse import quote

from django import forms
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe


class RangeSlider(forms.TextInput):
    def __init__(self, min_value, max_value, step, elem_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min = str(min_value)
        self.max = str(max_value)
        self.step = str(step)
        self.elem_name = str(elem_name)

    def render(self, name, value, attrs=None, renderer=None):
        input_id = 'id_{}'.format(name)
        value = value if value else '0'
        html = f"""
            <input type="range" id="{input_id}" name="{name}" value="{value}" 
                   step="{self.step}" min={self.min} max={self.max} 
                   data-rangeslider class='input-slider'>
            <br>
            <h5><strong><output class="output-slider"></output></strong></h5>
        """
        return mark_safe(html)


class ModelInitialTextWidget(forms.TextInput):
    def __init__(self, elem_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elem_name = str(elem_name)

    def render(self, name, value, attrs=None, renderer=None):
        html = """
        <p>{}</p>
        """.format(value)
        return mark_safe(html)


class EvidenceUrlChoicesWidget(widgets.ChoiceWidget):
    input_type = 'radio'
    template_name = 'django/forms/widgets/radio.html'
    option_template_name = 'django/forms/widgets/radio_option.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_id = None
        self.worker_id = None

    def render(self, name, value, attrs=None, renderer=None):  # noqa: too-many-locals
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        default_value = context.get('widget').get('value')[0]
        start_html = f"""
            <div id="div_id_{name}" class="form-group" value={default_value}>
            <div class="">
        """
        finish_html = """
            </div>
            </div>
        """
        html = start_html
        if context.get('widget').get('optgroups'):
            for choice in context.get('widget').get('optgroups'):
                subgroup = choice[1][0]
                index = int(subgroup.get('index')) + 1
                name = subgroup.get('name')
                label = subgroup.get('label')
                value = subgroup.get('value')

                is_checked = ''
                if default_value and value == default_value:
                    is_checked = 'checked="checked"'
                if value.startswith("http"):
                    href = quote(value)
                    href = reverse('workflow:redirect') + \
                        f'?to={href}&item_id={self.item_id}' \
                        f'&worker_id={self.worker_id}' \
                        f'&click_type=corroborating_link'
                    a_href_tag = f'<a target="_blank" href="{href}" ' \
                                 f'class="corroborating_link">{label}</a>'
                else:
                    a_href_tag = label
                if not value:
                    value = 'None'
                    label = subgroup.get('label')
                    a_href_tag = label
                    if not default_value:
                        is_checked = 'checked="checked"'
                html += f"""
                    <div class="form-check">
                        <label for="id_id_{name}_0_{index}" class="form-check-label">
                            <input type="radio" class="form-check-input" 
                                   name="{name}" {is_checked} id="id_id_{name}_0_{index}"
                                   value="{value}">
                            {a_href_tag}
                        </label>
                    </div>
                """
        html += finish_html
        return mark_safe(html)


class CorroboratingEvidenceWidget(forms.URLInput):
    def __init__(self, elem_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elem_name = str(elem_name)

    def render(self, name, value, attrs=None, renderer=None):
        html = """
        <p>{}</p>
        """.format(value)
        return mark_safe(html)
