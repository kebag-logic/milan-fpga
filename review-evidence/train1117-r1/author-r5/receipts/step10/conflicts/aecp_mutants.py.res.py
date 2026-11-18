R = ['import aecp_face_mutants\nimport aecp_notice_mutants\n',
     '    + tuple(defect(*row) for row in aecp_map_mutants.ROWS) + tuple(defect(*row) for row in aecp_face_mutants.ROWS) \\\n'
     '    + tuple(defect(*row) for row in aecp_notice_mutants.ROWS) \\\n']
