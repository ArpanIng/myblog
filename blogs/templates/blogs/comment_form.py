<h2>Add a new comment</h2>

<form action="{% url 'blogs:post_comment' post.id %}" method="post">
  {% csrf_token %} {{ form.as_p }}
  <p><input type="submit" value="Add Comment" /></p>
</form>
