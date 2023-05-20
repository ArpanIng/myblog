{% extends 'base.html' %}

{% block title %}Share a post{% endblock title %}

{% block content %}
{% if sent %}
<h1>Email successcully sent</h1>
<p>"{{ post.title }}" was successfully sent to {{ form.cleaned_data.to }}.</p>
{% else %}
<h1>Share "{{ post.title }}" by e-mail</h1>
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Send e-mail">
</form>
{% endif %}
{% endblock content %}