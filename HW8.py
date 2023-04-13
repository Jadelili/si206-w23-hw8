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
    ON restaurants.building_id = buildings.id''')
    building_list = cur.fetchall()
    cur.execute('''SELECT restaurants.name, restaurants.rating, categories.category FROM restaurants
    JOIN categories ON restaurants.category_id = categories.id''')
    cat_list = cur.fetchall()

    for building in building_list:
        inner_d = {}
        inner_d["building"] = building[1]
        outer_d[building[0]] = inner_d
    for cat in cat_list:
        inner_d = {}
        inner_d["category"] = cat[2]
        inner_d["rating"] = cat[1]
        outer_d[cat[0]].update(inner_d)
    # print(outer_d)
    return outer_d
    
    
def plot_rest_categories(db):
    outer_d = {}
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    cur.execute("SELECT categories.category, restaurants.category_id FROM categories JOIN restaurants ON categories.id = restaurants.category_id")
    cat_orig_list = cur.fetchall()

    cat_list = []
    for i in cat_orig_list:
        cat_list.append(i)

    d = {}
    for cat in cat_list:
        cur.execute("SELECT COUNT(*) FROM restaurants WHERE category_id = ?", (cat[1],))    # sqlite3.InterfaceError: Error binding parameter 0 - probably unsupported type.
        # fetchall returns a list of tuples (even with one tuple inside), whereas fetchone returns one thing (a tuple with 2+ elements) (don't have to access twice)
        count = cur.fetchone()
        d[cat[0]] = count[0]
    s_d = sorted(d.items(), key = lambda x:x[1])  # a list of tuples, not a dict
    

    fig = plt.figure(figsize=(8,5))
    # fig.tight_layout()
    plt.subplots_adjust(left=0.3, right=0.9, bottom=0.3, top=0.9, wspace=1, hspace=1)
    
    # ax = fig.add_subplot(111)
    # fig, ax = plt.subplots()
    plt.subplot(111)
    for i in s_d:
        plt.barh(i[0], i[1], color=("lightblue"))
    # for i in s_d:
    #     ax.barh(i[0], i[1], color=("lightblue"))

    # ax.set_title("Types of Restaurant on South University Ave")
    # ax.set_xlabel("Number of Restaurants")
    # ax.set_ylabel("Restaurant Categories")
    plt.suptitle("Types of Restaurant on South University Ave")   # add a centered supertitle
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")

    plt.show()
    return d


def find_rest_in_building(building_num, db):
    path = os.path.dirname(os.path.abspath(__file__))       # need to initiate each time ?
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    cur.execute('''SELECT restaurants.name, restaurants.rating FROM buildings JOIN restaurants ON buildings.id = restaurants.building_id 
                WHERE buildings.building = ?''', (building_num,))
    res_list = cur.fetchall()
    s_res_list = sorted(res_list, key = lambda x:x[1], reverse=True) 
    lst = []
    for i in s_res_list:
        lst.append(i[0])
    return lst


#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    path = os.path.dirname(os.path.abspath(__file__))       
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()                                     # sequence of from, join
    
    cur.execute("SELECT category FROM categories")
    cat_list = cur.fetchall()
    cur.execute("SELECT building FROM buildings")
    bud_list = cur.fetchall()
        
    rating_list1 = []
    rating_list2 = []
    for i in cat_list:
        cur.execute('''SELECT categories.category, AVG(restaurants.rating) FROM categories JOIN restaurants 
        ON categories.id = restaurants.category_id WHERE categories.category = ?''', (i[0],))
        rating1 = cur.fetchone()
        rating_list1.append(rating1)
    for j in bud_list:
        cur.execute('''SELECT buildings.building, AVG(restaurants.rating) FROM buildings JOIN restaurants 
        ON buildings.id = restaurants.building_id WHERE buildings.building = ?''', (j[0],))
        rating2 = cur.fetchone()
        rating_list2.append(rating2)

    rating_cat = sorted(rating_list1, key = lambda x:x[1])
    rating_bud = sorted(rating_list2, key = lambda x:x[1])
    # print(rating_bud)

    # fig1, ax1 = plt.subplot(121)            # subplots & add_subplot
    # for m in rating_cat:
    #     ax1.barh(round(m[1],2), m[0], color=("lightblue"))

    # fig2, ax2 = plt.subplot(122)
    # for n in rating_bud:
    #     ax2.barh(round(n[1],2), n[0], color=("lightblue"))
    # plt.show()

    fig = plt.figure(figsize=(8,8))
    fig.tight_layout()
    plt.subplots_adjust(left=0.3, right=0.9, bottom=0.3, top=0.9)
    plt.subplot(121)
    plt.suptitle("Average Restaurant Ratings by Category")
    plt.xlabel("Ratings")
    plt.ylabel("Categories")
    plt.xlim(0,5)
    for m in rating_cat:
        # print(m)
        plt.barh(m[0], round(m[1],1), color=("lightgreen"))
    
    plt.subplot(122)
    plt.suptitle("Average Restaurant Ratings by Building")
    plt.xlabel("Ratings")     #barh
    plt.ylabel("Buildings")
    plt.xlim(0,5)
    for n in rating_bud:
        # print(n)
        plt.barh(str(n[0]), round(n[1],1), color=("lightgreen"))
    plt.show()
    return [rating_cat[-1], rating_bud[-1]]



#Try calling your functions here
def main():
    # load_rest_data("South_U_Restaurants.db")
    plot_rest_categories("South_U_Restaurants.db")
    # find_rest_in_building(1140, "South_U_Restaurants.db")
    get_highest_rating("South_U_Restaurants.db")



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
    unittest.main(verbosity=2)