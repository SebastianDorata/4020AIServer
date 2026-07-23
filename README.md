# 4020AIServer

# DATASET ROWS WERE COMPLETELY INCORRECT, HAD TO FIND NEW DATASET.
Example:
<img width="624" height="42" alt="image" src="https://github.com/user-attachments/assets/3da66852-9324-4dc0-9651-fd8e515bb7b9" /> <br>
Turkey breast had absurd caloric and macro amounts per 100g. Some food items were missing too. Not good dataset.


NEW DATASET = https://www.kaggle.com/datasets/waltonj/usda-myfooddata-nutrition-facts-2020

Features:
Server has 3 pages: <br>
"/" - home page, get displays form, post submits it and goes to results page <br>
Results page, shows calculated vs generated calorie and macros <br>
"/about" - about page, student id details <br>

Server can take user attributes calculate TDEE, obtain target calories and macros. <br>
Can generate plan with those values and result page displays the targets, user info, and eventually meal plan. <br>

TO-DO:
- Change/style website again, uses an old project I made as a reference ✅
- Find new dataset with proper row data ✅
- Redo db/query logic ✅
- Potentially create comparison charts, calculated macros vs ai macros of meal plans, etc. ✅
- See how close ai-generated plan adheres to calorie targets and macro goals
- Connect to actual ai model to generate meal plans instead of using sample ones.
- Optimize current prompt maybe.

Explanation of script files: <br>
main.py - run this to run server, link is outputted in console<br>
import_food_aliases.py - ALREADY RAN DO NOT RUN AGAIN, adds food aliases to table in db<br>
import_foods.py - ALREADY RAN DO NOT RUN AGAIN, adds dataset info to foods table in db<br>
db.py - database<br>
forms.py - Where forms are being referenced from<br>
models.py - Table schemas<br>
routes.py - Routes for server urls, calculation logic, probably where we'll store AI-connection logic too.<br>



Images:
<img width="1393" height="924" alt="image" src="https://github.com/user-attachments/assets/0a26f73c-c213-48d7-a1e2-a416a583f5e4" />
<img width="1379" height="857" alt="image" src="https://github.com/user-attachments/assets/900385db-d861-4436-b670-9919dbeb3205" />
<img width="1367" height="908" alt="image" src="https://github.com/user-attachments/assets/e674ccf4-559f-4748-b574-8ca8dc0ea589" />
<img width="1222" height="915" alt="image" src="https://github.com/user-attachments/assets/290c24ad-b490-4b07-8c81-c617e4c6b428" />
<img width="921" height="796" alt="image" src="https://github.com/user-attachments/assets/31dba640-0bd4-4228-abb3-d0697e517360" />

[Installation Guide](docs/installation.md) - Docker & Ollama setup instruction



