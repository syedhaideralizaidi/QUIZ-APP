For Social Login using Google follow the documentation and use this in the template

{% load socialaccount %}


<form action="{% provider_login_url 'google' %}" method="post">
                  {% csrf_token %}
                   <button type="submit" class="btn btn-link" style="color: darkblue"><a href="{% url 'dashboard-student' %}" style="color: black"> <img src="{% static 'images/google.png' %}" alt="Google" height="50px">
                       Sign in with Google</a></button>
</form>



 <span>
                <button type="button" class="btn btn-link" style="color: black"><a href="{% url 'account_login' %}" style="color: black">
               <img src="{% static 'images/google.png' %}" alt="Google" height="50px">
              Login with Gmail</a></button>
</span>


To run on asgi server, run this command

daphne -b 127.0.0.1 quizapp.asgi:application
