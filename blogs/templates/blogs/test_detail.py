{% extends 'test_base.html' %}

{% block title %}{{ post.title }}{% endblock title %}

{% block content %}
<div class="row g-5">
  
  <div class="col-md-8">
    <h1 class="blog-post-title">{{ post.title }}</h1>
    <p class="blog-post-meta">
      {{ post.publish|date:'M j, o' }} by
      <a class="text-decoration-none text-secondary" href="#">{{ post.author }}</a>
    </p>
    <p>{{ post.body|linebreaks }}</p>
    <p>
      <a class="text-secondary" href="{% url 'blogs:post_share' post.id %}">Share this post</a>
    </p>
    <hr>
    {% with comments.count as total_comments %}
    <h4>{{ total_comments }} comment{{ total_comments|pluralize }}</h4>
    {% endwith %}
    {% for comment in comments %}
    <p>Comment {{ forloop.counter }} by {{ comment.name }} {{ comment.created }}</p>
    {{ comment.body|linebreaks  }}
    {% endfor %}
  </div>
  
  <div class="col-md-4">
    <div class="position-sticky" style="top: 2rem">
      <div class="p-4 mb-3 bg-body-tertiary rounded">
        <h4>Similar Posts</h4>
        {% for post in similar_posts %}
        <p class="mb-0">
          <a class="text-secondary text-decoration-none" href="{{ post.get_absolute_url }}">{{ post.title }}</a>
        </p>
        {% empty %}
        <p class="mb-0">There are no similar posts yet.</p>
        {% endfor %}
      </div>
    </div>
  </div>
  
</div>
{% endblock content %}