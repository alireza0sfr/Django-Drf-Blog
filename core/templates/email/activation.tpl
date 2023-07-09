{% extends "mail_templated/base.tpl" %}

{% block subject %}
Email Activation
{% endblock %}

{% block html %}
Token: {{ token }}
{% endblock %}