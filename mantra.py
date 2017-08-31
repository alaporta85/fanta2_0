import pickle


schemes = {'343':['P','Dc','Dc','Dc','E','M/C','M/C','E','W/A','A/Pc','W/A'],
           '3412':['P','Dc','Dc','Dc','E','M/C','M/C','E','T','A/Pc','A/Pc'],
           '3421':['P','Dc','Dc','Dc','E','M/C','M/C','E','T/W','T/W','A/Pc'],
           '352':['P','Dc','Dc','Dc','E/W','M/C','M','M/C','E','A/Pc','A/Pc'],
           '442':['P','Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','A/Pc','A/Pc'],
           '433':['P','Dd','Dc','Dc','Ds','M/C','M','M/C','W/A','A/Pc','W/A'],
           '4312':['P','Dd','Dc','Dc','Ds','M/C','M','M/C','T','A/Pc','A/Pc'],
           '4321':['P','Dd','Dc','Dc','Ds','M/C','M','M/C','T/W','T/W','A/Pc'],
           '4231':['P','Dd','Dc','Dc','Ds','M','M/C','T/W','T','T/W','A/Pc'],
           '4411':['P','Dd','Dc','Dc','Ds','E/W','M','M/C','E/W','T','A/Pc'],
           '4222':['P','Dd','Dc','Dc','Ds','M','M','W','T','A','A/Pc']}




caso1 = [('Day 1', 'HANDANOVIC', ['Por']), ('Day 1', 'ZAPPACOSTA', ['Dd','E']),
         ('Day 1', 'ROMAGNOLI', ['Dc']), ('Day 1', 'CHIELLINI', ['Ds','Dc']),
         ('Day 1', 'MASINA', ['Ds','E']), ('Day 1', 'MILINKOVIC-SAVIC', ['C','T']),
         ('Day 1', 'DE ROSSI', ['M','C']), ('Day 1', 'HAMSIK', ['C','T']),
         ('Day 1', 'CANDREVA', ['W']), ('Day 1', 'MILIK', ['Pc']),
         ('Day 1', 'BERARDI', ['A']), ('Day 1', 'QUAGLIARELLA', ['Pc']),
         ('Day 1', 'FALCINELLI', ['Pc']), ('Day 1', 'BIRSA', ['T']),
         ('Day 1', 'FELIPE ANDERSON', ['W','T']), ('Day 1', 'VERDI', ['T','A']),
         ('Day 1', 'IONITA', ['C','T']), ('Day 1', 'BENASSI', ['C']),
         ('Day 1', 'MAGNANELLI', ['M','C']), ('Day 1', 'CONTI', ['Dd','E']),
         ('Day 1', 'KOULIBALY', ['Dc']), ('Day 1', 'ASTORI', ['Dc']),
         ('Day 1', 'PADELLI', ['Por'])]

caso2 = [('Day 1', 'HANDANOVIC', ['Por']), ('Day 1', 'CONTI', ['Dd','E']),
         ('Day 1', 'KOULIBALY', ['Dc']), ('Day 1', 'CHIELLINI', ['Ds','Dc']),
         ('Day 1', 'MASINA', ['Ds','E']), ('Day 1', 'DE ROSSI', ['M','C']),
         ('Day 1', 'HAMSIK', ['C','T']),('Day 1', 'CANDREVA', ['W']),
         ('Day 1', 'BIRSA', ['T']), ('Day 1', 'FELIPE ANDERSON', ['W','T']),
         ('Day 1', 'QUAGLIARELLA', ['Pc']), ('Day 1', 'BERARDI', ['A']),
         ('Day 1', 'FALCINELLI', ['Pc']), ('Day 1', 'BENASSI', ['C']),
         ('Day 1', 'VERDI', ['T','A']), ('Day 1', 'MILINKOVIC-SAVIC', ['C','T']),
         ('Day 1', 'CASTRO', ['C','W']), ('Day 1', 'MAGNANELLI', ['M','C']),
         ('Day 1', 'ROMAGNOLI', ['Dc']), ('Day 1', 'ASTORI', ['Dc']),
         ('Day 1', 'ZAPPACOSTA', ['Dd','E']), ('Day 1', 'TOLOI', ['Dc']),
         ('Day 1', 'PADELLI', ['Por'])]

caso3 = [('Day 1', 'HANDANOVIC', ['Por']), ('Day 1', 'ASTORI', ['Dc']),
         ('Day 1', 'KOULIBALY', ['Dc']), ('Day 1', 'CHIELLINI', ['Ds','Dc']),
         ('Day 1', 'ZAPPACOSTA', ['Dd','E']), ('Day 1', 'MILINKOVIC-SAVIC', ['C','T']),
         ('Day 1', 'HAMSIK', ['C','T']),('Day 1', 'MASINA', ['Ds','E']),
         ('Day 1', 'BIRSA', ['T']), ('Day 1', 'QUAGLIARELLA', ['Pc']),
         ('Day 1', 'FALCINELLI', ['Pc']), ('Day 1', 'PADELLI', ['Por']),
         ('Day 1', 'MILIK', ['Pc']), ('Day 1', 'VERDI', ['T','A']),
         ('Day 1', 'BERARDI', ['A']), ('Day 1', 'IONITA', ['C','T']),
         ('Day 1', 'BENASSI', ['C']), ('Day 1', 'DE ROSSI', ['M','C']),
         ('Day 1', 'CANDREVA', ['W']),('Day 1', 'MAGNANELLI', ['M','C']),
         ('Day 1', 'ROMAGNOLI', ['Dc']), ('Day 1', 'TOLOI', ['Dc']),
         ('Day 1', 'LAXALT', ['E'])]

caso4 = [('Day 1', 'HANDANOVIC', ['Por']), ('Day 1', 'ZAPPACOSTA', ['Dd','E']),
         ('Day 1', 'ROMAGNOLI', ['Dc']), ('Day 1', 'KOULIBALY', ['Dc']),
         ('Day 1', 'CHIELLINI', ['Ds','Dc']), ('Day 1', 'MILINKOVIC-SAVIC', ['C','T']),
         ('Day 1', 'DE ROSSI', ['M','C']), ('Day 1', 'HAMSIK', ['C','T']),
         ('Day 1', 'CANDREVA', ['W']), ('Day 1', 'MILIK', ['Pc']),
         ('Day 1', 'BERARDI', ['A']), ('Day 1', 'FALCINELLI', ['Pc']),
         ('Day 1', 'QUAGLIARELLA', ['Pc']), ('Day 1', 'VERDI', ['T','A']),
         ('Day 1', 'BENASSI', ['C']), ('Day 1', 'MAGNANELLI', ['M','C']),
         ('Day 1', 'MASINA', ['Ds','E']), ('Day 1', 'BIRSA', ['T']),
         ('Day 1', 'IONITA', ['C','T']),('Day 1', 'LAXALT', ['E']),
         ('Day 1', 'ASTORI', ['Dc']),('Day 1', 'TOLOI', ['Dc']),
         ('Day 1', 'PADELLI', ['Por'])]

caso5 = [('Day 1', 'HANDANOVIC', ['Por']), ('Day 1', 'ZAPPACOSTA', ['Dd','E']),
         ('Day 1', 'KOULIBALY', ['Dc']), ('Day 1', 'CHIELLINI', ['Ds','Dc']),
         ('Day 1', 'MASINA', ['Ds','E']), ('Day 1', 'FELIPE ANDERSON', ['W','T']),
         ('Day 1', 'DE ROSSI', ['M','C']), ('Day 1', 'HAMSIK', ['C','T']),
         ('Day 1', 'CASTRO', ['C','W']), ('Day 1', 'QUAGLIARELLA', ['Pc']),
         ('Day 1', 'FALCINELLI', ['Pc']), ('Day 1', 'MILIK', ['Pc']),
         ('Day 1', 'BERARDI', ['A']), ('Day 1', 'BIRSA', ['T']),
         ('Day 1', 'CANDREVA', ['W']), ('Day 1', 'VERDI', ['T','A']),
         ('Day 1', 'MILINKOVIC-SAVIC', ['C','T']), ('Day 1', 'MAGNANELLI', ['M','C']),
         ('Day 1', 'ROMAGNOLI', ['Dc']),  ('Day 1', 'ASTORI', ['Dc']),
         ('Day 1', 'TOLOI', ['Dc']), ('Day 1', 'LAXALT', ['E']),
         ('Day 1', 'PADELLI', ['Por'])]

caso6 = [('Day 1', 'HANDANOVIC', ['Por']), ('Day 1', 'ROMAGNOLI', ['Dc']),
         ('Day 1', 'KOULIBALY', ['Dc']), ('Day 1', 'CHIELLINI', ['Ds','Dc']),
         ('Day 1', 'CONTI', ['Dd','E']),  ('Day 1', 'DE ROSSI', ['M','C']),
         ('Day 1', 'IONITA', ['C','T']), ('Day 1', 'ZAPPACOSTA', ['Dd','E']),
         ('Day 1', 'HAMSIK', ['C','T']), ('Day 1', 'FALCINELLI', ['Pc']),
         ('Day 1', 'BERARDI', ['A']), ('Day 1', 'MILIK', ['Pc']),
         ('Day 1', 'CASTRO', ['C','W']), ('Day 1', 'CANDREVA', ['W']),
         ('Day 1', 'FELIPE ANDERSON', ['W','T']), ('Day 1', 'MILINKOVIC-SAVIC', ['C','T']),
         ('Day 1', 'BENASSI', ['C']), ('Day 1', 'MAGNANELLI', ['M','C']),
         ('Day 1', 'BIRSA', ['T']),  ('Day 1', 'MASINA', ['Ds','E']),
         ('Day 1', 'ASTORI', ['Dc']), ('Day 1', 'VERDI', ['T','A']),
         ('Day 1', 'PADELLI', ['Por'])]

caso7 = [('Day 1', 'HANDANOVIC', ['Por']), ('Day 1', 'CONTI', ['Dd','E']),
         ('Day 1', 'ASTORI', ['Dc']), ('Day 1', 'TOLOI', ['Dc']),
         ('Day 1', 'MASINA', ['Ds','E']), ('Day 1', 'BENASSI', ['C']),
         ('Day 1', 'DE ROSSI', ['M','C']), ('Day 1', 'HAMSIK', ['C','T']),
         ('Day 1', 'BIRSA', ['T']), ('Day 1', 'FALCINELLI', ['Pc']),
         ('Day 1', 'VERDI', ['T','A']), ('Day 1', 'QUAGLIARELLA', ['Pc']),
         ('Day 1', 'BERARDI', ['A']), ('Day 1', 'CANDREVA', ['W']),
         ('Day 1', 'FELIPE ANDERSON', ['W','T']), ('Day 1', 'MAGNANELLI', ['M','C']),
         ('Day 1', 'CASTRO', ['C','W']), ('Day 1', 'IONITA', ['C','T']),
         ('Day 1', 'LAXALT', ['E']), ('Day 1', 'MILINKOVIC-SAVIC', ['C','T']),
         ('Day 1', 'ZAPPACOSTA', ['Dd','E']), ('Day 1', 'CHIELLINI', ['Ds','Dc']),
         ('Day 1', 'PADELLI', ['Por'])]





























