

# Validation

Mobile testing came back with satisfactory results.


# Deployment

The project was created using the Code Institute Python template provided and was deployed through Heroku.

## Heroku Deployment

- Login / Sing up to Heroku
- Select “New” followed by “Create New App” from the main dashboard page
- Give the project a unique name (important) and select a region
- This will then create the app and then redirect you to the deploy tab. From the top submenu navigate to the settings tab.
- In this case since the Code Institute template was used a special config var needed to be set up in order for the app to function. You might not need this unless you have sensitive information you would not like to share.
- Once in the config var section select the reveal button. This will show the current config vars for the app (should be empty if it is new)
- Next within the KEY input field type PORT (use caps) and then in the VALUE field type 8000 and select the add button.
- The next step is to select add buildpack by selecting the button below config vars.
- The order of the next steps is important. First select add Python in the pop-up window and then save.
- Next repeat the steps but select node.js this time, remember the order is important so in the list you should see python first then node.js.
- Next, using the submenu tab navigate to the deploy section.
- Within the deployment method section choose GitHub followed by the connect to GitHub button and follow the steps prompted in order to do so.
- Next select the correct account and enter the repository name that you want to deploy. Once the search is completed select connect.
- This will then connect both the chosen repository and Heroku. Below this will be the deploy method section where you can choose to automatically or manually deploy your project.
- You must select the correct branch to do so. In the example main was selected then automatic deployment.
- By doing this any commits from GitHub will automatically reflect onto the Heroku account.
- Heroku will now create the app. Once this process is complete you will see a message “Your App Was Successfully Deployed” and a link to the live site.

***

# Credits

## Game Idea

- Tech With Tim (Youtube)

## Slow Print Function

- gunton: slowprint.py (HitHub)

## Code Help

- Love Sandwhiches
- W3S
- Stack Overflow

***

# Acknowledgements

A huge thank you to my mentor Victor Miclovich
