from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:

            response = client.post("/api/new-game")
            json = response.get_json()

            self.assertEqual(type(json["gameId"]),str)
            self.assertEqual(type(json["board"]),list)
            self.assertEqual(json["gameId"] in games, True)



            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:
            # simulate new game POST request and extract values
            start_response = client.post('/api/new-game')
            start_json = start_response.get_json()
            start_json_gameId = start_json["gameId"]

            # extract test game from games dictionary and manually adjust board
            #TODO: some will say hard-code grid explictly
            games[start_json_gameId].board = [list('APPLE') for row in range(5)]


            score_response_ok = client.post('/api/score-word',
                                   json={ "word" : "APPLE",
                                         'game_id' : start_json_gameId}).get_json()

            score_response_not_board = client.post('/api/score-word',
                                   json={ "word" : "UPHOLD",
                                         'game_id' : start_json_gameId}).get_json()

            score_response_not_word = client.post('/api/score-word',
                                   json={ "word" : "XXX",
                                   'game_id' : start_json_gameId}).get_json()


            self.assertEqual(score_response_ok, {"result": "ok"})
            self.assertEqual(score_response_not_board, {"result": "not-on-board"})
            self.assertEqual(score_response_not_word, {"result": "not-word"})


            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}

