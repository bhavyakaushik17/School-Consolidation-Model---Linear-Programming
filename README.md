# School Consolidation Model - Linear Programming
School consolidation is an act of merging relatively smaller schools with the nearby schools in order to give good facilities and minimize multi-grade teaching, a prevalent issue in the rural areas of Andhra Pradesh, India.

The given data is about schools in a small district named Chittoor. We have the geographical coordinates of the schools, their locality code, and the number of students enrolled. The model gives the output of the school status (open/close), total students in each grade of the open schools, the number of students transferred from old school to new school.

The model has various constraints explained as follows:
1. Access constraint: It ensures that the students do not travel a maximum additional distance D1.
2. Logical constraints: It ensures that transfer only takes place to one open school from any number of the closed schools.
3. Small school closing constraint: It forces those small schools to close that have low enrolment and have its nearest school within D3 distance.
4. Large school opening constraint: It forces large schools to open if they are more than D2 from each other (Kept as an option right now).
5. No school distance constraint: There will be at most one school within D2.
6. Flow balance constraint: It ensures that all students are allocated to schools and to the same grade.
7. Capacity constraint: It ensures that the total students in any grade after consolidation does not exceed the capacity.
