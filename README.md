# 4020AIServer

# LOTS OF REWORKING NEEDS TO BE DONE
# DATASET ROWS ARE COMPLETELY INCORRECT, NEED TO FIND NEW DATASET.
Which means I need to rework, tables/rows, sql logic, etc.

Features so far although sample meal calories and macros are incorrect because database values are insane:

Server has 3 pages:
"/" - home page, get displays form, post submits it and goes to results page
"/about" - about page, student id details

Server can take user attributes calculate TDEE, obtain target calories and macros. 
Can generate plan with those values and result page displays the targets, user info, and eventually meal plan.

TO-DO:
- Change/style website again, uses an old project I made as a reference
- Find new dataset with proper row data
- Redo db/query logic
- Potentially create comparison charts, calculated macros vs ai macros of meal plans, etc.
- See how close ai-generated plan adheres to calorie targets and macro goals
- Connect to actual ai model to generate meal plans instead of using sample ones.
- Optimize current prompt maybe.
