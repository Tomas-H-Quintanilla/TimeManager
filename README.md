# Description of the project

The project consists of a Timetracker application (whose name is Timemanger). In this application you can create and manage projects and then assign tasks that have a content (text) and a time assigned to them.

## Creating a User

You can register as a user, giving your information at the Register page, then you login using the password you defined.

## Projects tab

Before entering any tasks, you need to have at least a project assigned, either created by you or by another person. Go to the projects tab to overview the project you are involved in.

To create a project, you just need to Enter a title and select the members to be involved. You can click on the porject list to see the details.

If you are the manager of the project, you will be able to download all the tasks in the project that you selected and remove or add members to it, as well as changing its name, or deleting it.

If you are not the manager of the project, you will be able to download the information about the tasks you have done in the project you have clicked on.

## Tasks tab

You have three options if you want to enter tasks:

1 - Use a cronometer starting and pausing it when you want to measure the time you spent on a task.

2 - Use the manual approach, entering the date that the task is gonna be registered and the time spent on it.

3 - Use the file option. You can upload a csv file, in which the files requested by the form shall be separated by "," and the dates must have the format dd/mm/YYYY or dd-mm-YYYY

Once you enter a task, you will be able to see it on the right part of the screen, using the different time filters to view the tasks. If you click on a task you can edit the stored information about it.

## Profile tab

If you click on the nav button "Profile" or on your name on the top of the screen, you will be able to edit your personal data, as well as you will have a list of the projects you are involved in. If you click the download button, you will be able to download the tasks you did within the period defined by the nav buttons above the download button.

## Manager tab

If you are a super user (See documentation on Django super users here https://djangocentral.com/creating-super-user-in-django/) you will have access to the manager options near the logout button. This tab allow you to download all the tasks done by a worker registered in the app and all the tasks corresponding to a certain project, allowing you to use different time filters to do so.

## Deploying the app

This is a Django project, so you need the framework in your server to support it. Follow the guide here in order to deploy the server: https://docs.djangoproject.com/en/3.1/howto/deployment/.

The project will create a SQLite database by default, if you want to change the database in use you can do so following this guide: https://docs.djangoproject.com/en/3.1/ref/databases/.

For any questions or notes for improvement, please feel free to contact me.
