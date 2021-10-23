from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import random
import xlrd
import os
import openpyxl
from datetime import datetime
from numba import jit
import tkinter as tk


df = pd.read_csv(r'likes history.csv',sep =';')
print(df.columns)
print(df)
print(df['date'])
