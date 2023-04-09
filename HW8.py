# Your name: Xiaoyi Li
# Your student id: 20937100
# Your email: jadeli@umich.edu
# List who you have worked with on this homework: None

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    outer_d = {}
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    cur.execute('''SELECT restaurants.name, buildings.building FROM restaurants JOIN buildings
    ON restaurants.category_id = buildings.id''')
    building_list = cur.fetchall()
    cur.execute('''SELECT restaurants.name, restaurants.rating, categories.category FROM restaurants
    JOIN categories ON restaurants.building_id = categories.id''')
    cat_list = cur.fetchall()
    for building in building_list:
        inner_d = {}
        inner_d["building"] = building[1]
        # if building[0] not in outer_d.keys():
        outer_d[building[0]] = inner_d
        # else:
        #     print(outer_d)
        #     outer_d[building[0]].append(inner_d)
    for cat in cat_list:
        inner_d = {}
        inner_d["category"] = cat[2]
        inner_d["rating"] = cat[1]
        # if cat[0] not in outer_d.keys():
        outer_d[cat[0]] = inner_d
        # else:
        #     outer_d[cat[0]].append(inner_d)
    print(outer_d)
    # for building in building_list:
    #     inner_d = {}
    #     inner_d["building"] = building[1]
    #     # if building[0] not in outer_d.keys():
    #     outer_d[building[0]] = inner_d
    #     # else:
    #     #     outer_d[building[0]]
    # for cat in cat_list:
    #     c_inner_d = {}
    #     c_inner_d["category"] = cat[2]
    #     c_inner_d["rating"] = cat[1]
    #     outer_d[cat[0]] = c_inner_d
    # print(outer_d)

    # for building in building_list:
    #     # b_inner_d = {}
    #     new_d = {}
    #     new_d["building"] = building[1]
    #     b_inner_d = outer_d.get(building[0], {})
    #     b_inner_d.update(new_d)
    #     outer_d[building[0]] = b_inner_d
    # for cat in cat_list:
    #     new_d = {}
    #     c_inner_d = {}
    #     new_d["category"] = cat[2]
    #     new_d["rating"] = cat[1]
    #     c_inner_d = outer_d.get(building[0], {})
    #     c_inner_d.update(new_d)
    #     outer_d[building[0]] = c_inner_d
    # for cat in cat_list:
    #     c_inner_d = {}
    #     c_inner_d["category"] = cat[2]
    #     c_inner_d["rating"] = cat[1]
    #     outer_d[building[0]] = c_inner_d
    # print(outer_d)


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    pass

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    load_rest_data("South_U_Restaurants.db")

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    # unittest.main(verbosity=2)
