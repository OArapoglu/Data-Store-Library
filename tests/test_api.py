from app import app

API_KEY = "bWFnZ2llOnN1bW1lcnk="

def test_index():
    """Test index directory endpoint."""
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.data == b'"Data Store Library"\n'


def test_api_key():
    """Test api_key."""
    response = app.test_client().get("/put")
    assert response.status_code == 400


def test_put1_json():
    """Test put for 1 json file."""
    response = app.test_client().get(
        f"/put?api_key={API_KEY}"
        + """&records=[{"key":1, "value":"test_value1"}]"""
        + """&files=[{"file_type":'JSON', 'name': 'test1.json'}]"""
        + """&destinations=[{"path":"local_files", "destination_type":"LOCAL" }]"""
    )
    assert response.status_code == 200

def test_update1_json():
    """Test update for 1 json file."""
    response = app.test_client().get(
        f"/update?api_key={API_KEY}"
        + """&records=[{"key":1, "value":"test_value11"}]"""
    )
    assert response.status_code == 200

def test_put1_xml():
    """Test put for 1 xml file."""
    response = app.test_client().get(
        f"/put?api_key={API_KEY}"
        + """&records=[{"key":2, "value":"test_value2"}]"""
        + """&files=[{"file_type":'XML', 'name': 'test2.xml'}]"""
        + """&destinations=[{"path":"local_files", "destination_type":"LOCAL" }]"""
    )
    assert response.status_code == 200

def test_update1_xml():
    """Test update for 1 xml file """
    response = app.test_client().get(
        f"/update?api_key={API_KEY}"
        + """&records=[{"key":2, "value":"test_value22"}]"""
    )
    assert response.status_code == 200

def test_delete2():
    """Test delete for 2 files."""
    response = app.test_client().get(
        f"/delete?api_key={API_KEY}"
        + """&record_keys=[1,2]"""
    )
    assert response.status_code == 200


def test_put2_xml_json():
    """Test put for 1 xml and 1 json files"""
    response = app.test_client().get(
        f"/put?api_key={API_KEY}"
        + """&records=[{"key":1, "value":"test_value1"}]"""
        + """&files=[{"file_type":'JSON', 'name': 'test1.json'}, {"file_type":'XML', 'name': 'test1.xml'}]"""
        + """&destinations=[{"path":"local_files", "destination_type":"LOCAL" }]"""
    )
    assert response.status_code == 200

def test_put3_xml_json():
    """Test put for 1 xml and 2 json files."""
    response = app.test_client().get(
        f"/put?api_key={API_KEY}"
        + """&records=[{"key":2, "value":"test_value2"}]"""
        + """&files=[{"file_type":'JSON', 'name': 'test2.json'}, {"file_type":'XML', 'name': 'test2.xml'}, {"file_type":'XML', 'name': 'test3.xml'}]"""
        + """&destinations=[{"path":"local_files", "destination_type":"LOCAL" }]"""
    )
    assert response.status_code == 200

def test_filter_records():
    """Test filter records"""
    response = app.test_client().get(
        f"/filter_records?api_key={API_KEY}"
        + "&value=test_value1"
        + "&limit=4"
        + "&offset=2"
    )
    assert response.status_code == 200

def test_delete5_files():
    """Test delete for 5 files."""
    response = app.test_client().get(
        f"/delete?api_key={API_KEY}"
        + """&record_keys=[1,2]"""
    )
    assert response.status_code == 200
