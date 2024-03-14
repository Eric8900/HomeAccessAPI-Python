# Katy ISD Home Access Center API

This is a custom HAC API for Katy ISD that I created using Python, Flask, Beautiful Soup, and requests-html. There is only one path for the API as it is specifically made for my Grade Calculator App to calculate the lowest grade needed to keep a specific grade. 

I might expand this later if I need.

# Documentation

## /
- This is the vercel home page

## /api
- This is the API home page and shows you the possible routes (which is not many)

## /api/getGrades
Fields: username='' | password=''

Example: https://home-access-api-python.vercel.app/api/getGrades?username=K1111111&password=PASSWORD

Returns a JSON with the following:
- "names":
  - Indexes of class names correspond with the array of "grades"
- "grades":
  - 3D Array in the following layout: <strong>grades[1][2][3]</strong>
  - 1 : <strong>[ Corresponding Index With Names Array ]</strong>
  - 2 : <strong>[ Major (0), Minor (1), Other (2) ]</strong>
  - 3 : <strong>[ Student's Points (0), Maximum Points (1), Percent (2), Category Weight (3), Category Points (4) ]</strong>

<img width="1434" alt="image" src="https://github.com/Eric8900/HomeAccessAPI-Python/assets/89477025/91a8ff1a-89ee-4fba-8d27-7fb4c3d94a38">

### The '/api/getGrades' route only captures the area in the red box (besides the name of the class)
- Cyan represents the second dimesion of the 'grades' array -> Values 0-2
- Magenta represents the third dimension of the 'grades' array -> Values 0-4
