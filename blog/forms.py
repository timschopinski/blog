from django import forms
from.models import Comment, Post

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your Name:",
            "user_email": "Your Email:",
            "text": "Your Comment:"
        }
        error_messages = {
            "user_name": {
              "required": "Your name must not be empty!",
              "max_length": "Please enter a shorter name!"
            }
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ["date", "slug"]


        error_messages = {
            "author": {
              "required": "Your name must not be empty!",
              "max_length": "Please enter a shorter name!"
            },
            "title": {
                "required": "Your title must not be empty!",
                "max_length": "Please enter a shorter title!"
            }
        }