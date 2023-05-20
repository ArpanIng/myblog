{% extends 'base.html' %}
{% block title %}My Blog{% endblock title %}

{% block content %}
<h1>My Blog</h1>
{% if tag %}
    <h2>Posts tagged with "{{ tag.name }}"</h2>
{% endif %}
{% for post in posts %}
    <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
    <p class="tags">Tags:
        {% for tag in post.tags.all %}
        <a href="{% url 'blogs:post_list_by_tag' tag.slug %}">{{ tag.name }}</a>
        {% if not foorloop.last %}, {% endif %}
        {% endfor %}
    </p>
    <p class="date">
        Published {{ post.publish }} by {{ post.author }}
    </p>
    {{ post.body|truncatewords:30|linebreaks }}
{% endfor %}
{% include 'pagination.html' with page=posts %}
{% endblock content %}
