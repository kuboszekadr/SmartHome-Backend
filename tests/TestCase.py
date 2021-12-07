from flaskr import create_app


class TestCase():

    @classmethod
    def setUpClass(cls):
        cls.app = create_app({'TESTING': True})
        cls.client = cls.app.test_client()
        cls._ctx = cls.app.test_request_context()
        cls._ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        db.get_engine(cls.app).dispose()

    def setUp(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self._ctx.pop() 