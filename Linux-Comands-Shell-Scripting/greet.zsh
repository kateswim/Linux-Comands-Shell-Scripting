#!/bin/zsh
# This script accepts the user's name and prints a greeting message

# Print the prompt message on screen
echo -n "Enter your name : "

# Wait for user to enter a name, and save the entered name into the variable 'name'
read name

# Print the welcome message followed by the name
echo "Welcome $name"

# Print the congratulatory message
echo -n "Congratulations! You just created and ran your first shell script "
echo "using Zsh on IBM Skills Network"

