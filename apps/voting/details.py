{% for question in questions %}
            <form method="post" action="" id="{{ question.id }}" class="poll-form">
            	{% csrf_token %}
            	<h3>{{question}}</h3>
            	{% for choice in choices %}
            	<div class="form-group">
            		<label><input type="radio" name="poll-choice" value="{{ choice.id }}"> {{ choice }}</label>
            	</div>
            	{% endfor %}
            	<input type="submit" value="Vote" class="btn btn-success">
            	<input type="button" class="btn btn-primary" value="Result">
            	<input type="hidden" name="question-id" value="{{ question.id }}">
            	<input type="hidden" name="submit-vote" value="1">
            	<input type="hidden" name="site-url" value="{{ request.get_full_path }}">
            </form>
            {% endfor %}