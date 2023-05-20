{% extends 'base.html' %}

{% block title %}{{ post.title }}{% endblock title %}

{% block content %}
<h1>{{ post.title }}</h1>
<p class="date">
    Published {{ post.publish }} by {{ post.author }}
</p>
{{ post.body|linebreaks }}
<p><a href="{% url 'blogs:post_share' post.id %}">Share this post</a></p>
<h2>Similar posts</h2>
{% for post in similar_posts %}
<p><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></p>
{% empty %}
There are no similar posts yet.
{% endfor %}
{% with comments.count as total_comments %}
<h2>{{ total_comments }} comment{{ total_comments|pluralize }}</h2>
{% endwith %}
{% for comment in comments %}
    <div class="comment">
        <p class="info">
            Comment {{ forloop.counter }} by {{ comment.name }}
            {{ comment.created }}
        </p>
        {{ comment.body|linebreaks }}
    </div>
{% empty %}
    <p>There are no comments.</p>
{% endfor %}
{% include 'blogs/comment_form.html' %}
{% endblock content %}