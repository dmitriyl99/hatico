rs.initiate();

while (!rs.isMaster().ismaster) {
  sleep(100);
}

db.attributes.insertMany([
  {
    "name": "is_animal_there",
    "desc": "есть животное",
    "values": [
      {
        "raw": "no",
        "desc": "нет",
      },
      {
        "raw": "yes",
        "desc": "да",
      },
    ]
  },
  {
    "name": "is_it_a_dog",
    "desc": "это собака",
    "values": [
      {
        "raw": "no",
        "desc": "нет",
      },
      {
        "raw": "yes",
        "desc": "да",
      },
    ]
  },
  {
    "name": "is_the_owner_there",
    "desc": "есть хозяин",
    "values": [
      {
        "raw": "no",
        "desc": "нет",
      },
      {
        "raw": "yes",
        "desc": "да",
      },
    ]
  },
  {
    "name": "color",
    "desc": "цвет",
    "values": [
      {
        "raw": "undefined",
        "desc": "не определено",
      },
      {
        "raw": "dark",
        "desc": "тёмный",
      },
      {
        "raw": "light",
        "desc": "светлый",
      },
      {
        "raw": "mixed",
        "desc": "смешанный",
      },
    ]
  },
  {
    "name": "tail",
    "desc": "хвост",
    "values": [
      {
        "raw": "undefined",
        "desc": "не определено",
      },
      {
        "raw": "short/absent",
        "desc": "короткий/отсутствует",
      },
      {
        "raw": "long",
        "desc": "длинный",
      },
    ]
  },
  {
    "name": "breed",
    "desc": "порода"
  }
])

db.attributes.createIndex( { "name": 1 }, { unique: true } )
