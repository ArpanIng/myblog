{% extends 'base.html' %}

{% block title %}Add a title{% endblock title %}

{% block content %}
{% if comment %}
    <h2>Your comment has been added.</h2>
    <p><a href="{{ post.get_absolute_url }}">Back to the post</a></p>
{% else %}
    {% include 'blogs/comment_form.html' %}
{% endif %}
{% endblock content %}
