# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:44:49 2017

@author: Bhavya
"""

 m=44;
 s=588;
 g=2;
//  SheetConnection Capacity("AP_trimmed.xlsx");
  SheetConnection distances("Kurnool_UP_6_7.xlsx");
  SheetConnection total_enrolment("Kurnool_UP_6_7.xlsx");
  SheetConnection total_students("Kurnool_UP_6_7.xlsx");
  //all sheets

// a from SheetRead (total_enrolment,"priority");
excelDistance from SheetRead (distances,"distance_schools");
excelEnrolment from SheetRead (total_enrolment,"enrolment");
 schoolTotal from SheetRead(distances,"schoolMandal");
// capacity from SheetRead (Capacity,"school_capacity");
//Dmin from SheetRead (distances,"min_distance");

excelStudents to SheetWrite (total_students,"final_students");
z to SheetWrite (total_students,"final_status");

 D1=3000;
 D2=3000;
//D3=900;
//p=10;
M=100000;
//Nmin=20;
Nmax=30;
