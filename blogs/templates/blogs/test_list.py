{% extends 'test_base.html' %}

{% block title %}My Blog{% endblock title %}

{% block content %}
<div class="row g-5">
  <div class="col-md-8">
    
    {% for post in posts %}
    <article class="blog-post">
      <h2 class="blog-post-title mb-1">
        <a
          class="text-decoration-none text-dark"
          href="{{ post.get_absolute_url }}"
        >
          {{ post.title }}</a
        >
      </h2>
      {% if tag %}
      <p>Posts {{ tag.name }}</p>
      {% endif %}
      <p class="blog-post-meta">
        {{ post.publish|date:'M j, o' }} by
        <a class="text-decoration-none text-secondary" href="#">{{ post.author }}</a>
      </p>
      <p>{{ post.body|truncatewords:30|linebreaks }}</p>
      <hr />
    </article>
    {% endfor %}

  </div>
  {% include 'sidebar.html' %}
  {% include 'pagination.html' with page=posts %}
</div>
{% endblock content %}
