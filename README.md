[![pypi][pypi]][pypi-url]
![python][python]
![license][license]
[![Docker pulls](https://img.shields.io/docker/pulls/mayanedms/mayanedms.svg?maxAge=3600)](https://hub.docker.com/r/mayanedms/mayanedms/)
[![Docker Stars](https://img.shields.io/docker/stars/mayanedms/mayanedms.svg?maxAge=3600)](https://hub.docker.com/r/mayanedms/mayanedms/)
[![Commits][commits]][commits-url]
[![Support][support]][support-url]
[![Store](https://img.shields.io/badge/Online_store-black)](https://teespring.com/stores/mayan-edms)
[![Donation](https://img.shields.io/badge/donation-PayPal-brightgreen)](https://paypal.me/MayanEDMS)


[pypi]: https://img.shields.io/pypi/v/mayan-edms.svg
[pypi-url]: https://pypi.org/project/mayan-edms/

[builds]: https://gitlab.com/mayan-edms/mayan-edms/badges/master/build.svg
[builds-url]: https://gitlab.com/mayan-edms/mayan-edms/pipelines

[python]: https://img.shields.io/pypi/pyversions/mayan-edms.svg
[python-url]: https://img.shields.io/pypi/l/mayan-edms.svg?style=flat

[license]: https://img.shields.io/pypi/l/mayan-edms.svg?style=flat
[license-url]: https://gitlab.com/mayan-edms/mayan-edms/blob/master/LICENSE

[commits]:  https://img.shields.io/github/commit-activity/y/mayan-edms/mayan-edms.svg
[commits-url]: https://gitlab.com/mayan-edms/mayan-edms/

[support]: https://img.shields.io/badge/Get_support-brightgreen
[support-url]: https://www.mayan-edms.com/support/

<div align="center">
  <a href="http://www.mayan-edms.com">
    <img width="200" heigth="200" src="https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/mayan_logo.png">
  </a>
  <br>
  <br>
  <p>
    Mayan EDMS is a document management system. Its main purpose is to store,
    introspect, and categorize files, with a strong emphasis on preserving the
    contextual and business information of documents. It can also OCR, preview,
    label, sign, send, and receive thoses files. Other features of interest
    are its workflow system, role based access control, and REST API.
  <p>

<p align="center">
    <img width="400" src="https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/overview.gif">
</p>
</div>
<div>
<h2 align="center">Manual Testing</h2>

Manual testing script can be found in this link: https://docs.google.com/document/d/1Xy7My4wbPAb79oHEmB09VubXXCQZUkHSMnN2aGcK5Vw/edit?usp=sharing 

<h2 align="center">Documentation</h2>

<h3 align="left">Task and Motivation</h3>
A new feature has been introduced to the Mayan dashboard that will help the CMU admissions committee sift through the many graduate applications they receive. The applications received will be stored in an "application dashboard" where an admin role can assign reviewers to specific applications and manage the reviewers as well. By introducing a centralized application storage and management dashboard, the committee will be able to review the applications more efficiently and in an organized manner. 

<h3 align="left">Requirements</h3>
The client did not have any specific requirements other than this new system being "less garbage" than the current system, which the faculty complains is very difficult to use to evaluate applicants and manage the applications. The three possible features to better the user experience would be to create 
  
  1) A dashboard or pane for reviewer assignment and management.

  2) A form for reviewers to enter and score candidates along various (custom/admissions-specific) directions, to be saved and possibly aggregated across multiple reviewers.

  3) A dashboard or pane for aggregating and displaying statistics, like average review score per candidate; average review score per reviewer; or other aggregate statistics for the applicant pool.

  This project is focused around creating a dashboard or pane for reviewer assignment and management. The primary goals we kept in mind while implementing our solution was to ensure modularity and make sure the user experience is very straightforward while still being able to get the product developed for the client on time.

<h3 align="left">Design</h3>

<h4 align=”left”>Application Dashboard</h4>
We have built this on top of the Mayan EDMS open source software since it is a good document management platform and allows for tagging which will come in handy when creating reviewers. There are a lot of reusable modules within the Mayan framework that we believe would be useful in implementing this dashboard especially given the sprint deadlines. The Mayan architecture involves using widgets to modularize the various actions regarding documents and teams such as viewing all documents, total groups, and documents in trash. We decided to use the existing code to create a new widget called “Application Dashboard” that would host our dashboard page where the admin can manage and assign reviewers to specific applications. 

<h4 align=”left”>Reviewers</h4>
There is also a menu sidebar that allows the user to navigate through and execute various actions regarding documents such as uploading documents, assigning them tags, and creating cabinets. The “tags” app on the menu allows the user to create new tags, delete old tags, and assign existing tags to documents. Since the admin would want to manage reviewers in general and not only in the context of specific applications, we decided to include a “reviewers” app on the menu. This reviewer functionality was based off of the tag app functionality. There were a couple reasons why we made this design decision - we wanted to implement a baseline version of the reviewer functionality by the end of the sprint to be able to show the client a test version of how we were creating the dashboard for them. Furthermore, our understanding of how the admin would use reviewers would be to assign them roles and permissions to view applications, to assign them to specific applications, and add/remove reviewers generally. Other than assigning them roles, the tag app already provides this functionality so reusing the tag framework would allow us to create a testable prototype of the final dashboard.  

<h4 align=”left”>Pages</h4>
Each widget has its own page and url associated with it which allows page redirection from various widgets and the homepage. We used the current url redirection logic to introduce the reviewer pages and application dashboard page to assign reviewers to documents.

<h3 align="left">Functionality</h3>
A bulk of the modifications were made within the documents and tags apps within the Mayan codebase. Most widgets and applications in the Mayan framework have an apps.py, views.py, and urls.py file which control what the user will see on the page, what messages the user will see on their screen after they have completed certain actions on the page, and where the user will be redirected to when they click on the links and buttons on the page. 

We did not create a new app for the creation of this application dashboard and instead modified the widgets and above-mentioned python files to introduce the “Application Dashboard” interface. The “Application Dashboard” was created as a widget within the documents app; hence, the documents app hosts all the dashboard pages and views which can be found in dashboard_widgets.py, application_document_views.py, and url.py. We decided to simply introduce this as another documents feature instead of creating a whole other app for it because we assumed that the admin’s primary focus is the application and managing them and the current document app in Mayan has a lot of functionalities such as seeing the total documents, checked out documents, and new documents. So, we decided to keep the “Application Dashboard” as another documents feature that the user could use if desired. 

The other large aspect of this implementation was creating the reviewer roles and assignments. As mentioned in the Design section above, we decided to use the tag app to create reviewer “tags” to allow a very straightforward reviewer assignment and management since the current implementation already allows the user to create new tags, attach tags to specific documents, delete tags, and perform bulk action on tags. Therefore, we have just introduced another set of tags that we call reviewers within this app and have “tags'' be the underlying component behind reviewers. Within the views.py file in the “tags” directory, there are classes for the “Reviewer tags” to modify them such as ReviewerAddActionView, ReviewerCreateView, and ReviewerDeleteActionView (there are others as well). These have the message pop ups regarding the user’s most recent action (such as deleting a reviewer). There are also links and urls associated with these classes and pages that allow the user to navigate between these pages from the sidebar and application dashboard (specifically in apps.py, links.py, url.py). We have also used the tag form to create a reviewer form that allows the admin to select multiple reviewers at a time when assigning/removing/deleting reviewers (forms.py). Because we were reusing the tag infrastructure, we needed to ensure that the labels of these groups of tags would be “reviewers’ instead of tags (models.py). Not creating this distinction could potentially cause the admin and users to be confused about tags vs reviewers and make the assignment and management process jumbled up with all the tag functionality. 

We also made a few design changes - specifically adding a reviewers icon to help visually distinguish reviewers from tags. Most of the functionality for such icons within the Mayan dashboard is controlled by the icons.py, links.py, and menus.py. There are slight variations in the icons for reviewers, adding reviewers, deleting reviewers, and creating reviewers which have been added in the icons.py for tags. Please refer to the manual testing document to see the actual icons. To actually link these icons to their respective tabs in the menus and pages, we modified the links.py and menus.py file to include the appropriate reviewer icons with their respective tag icon counterparts. 

<h3 align="left">Future Work</h3>
There is still definitely a lot of work to be done to make this a state of the art application dashboard. Firstly, we would like to separate reviewers and tags completely so that the reviewer functionality can be a lot more developed and not be restricted by the tag functionality. Ideally, we would create a separate app for it and then link this to all the existing pages that use reviewers. We would also like to make the dashboard and applications on the dashboard more visually informative such as adding a status bar or symbol on the top right corner of each application to show whether the application has been assigned reviewers, whether the application is in the process of being reviewed, and whether the application is done being reviewed. We would also like to develop the reviewer interface which would be very similar to the current admin interface with some fewer functionalities such as being able to assign and remove reviewers from an assignment. In general, there is room for our implementation to be more visually appealing as well like including a new logo for the application dashboard that is more information about what this dashboard is for.

</div>




