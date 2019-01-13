
import json
import sys


class Prioritizer:

    def __init__(self, weights):
        self.cnfg = weights

    def _confine_weights(self, cnfg, project_path):
        ''' Recursive deepth-first backtracking '''
        step = project_path[0]
        if len(project_path) > 1:
            if step in cnfg.keys():
                return self._confine_weights(cnfg[step], project_path[1:])

        current_weights = None
        try:
            current_weights = cnfg[step]['weights']
        except KeyError:
            pass

        return current_weights

    def cease(self, task, rc=0, msg=""):
        print(json.dumps(task))
        print(msg)
        sys.exit(rc)

    def _calculate(self, task):
        weights = self._confine_weights(self.cnfg['root'],
                                        task['project'].split('.'))

        if not weights:
            try:
                weights = self.cnfg['root']['weights']
            except KeyError:
                self.cease(task, rc=1,
                           msg='Inconsistent weights cnfg. No global default.')

        sub_prios = []
        for key, val in weights.items():
            try:
                sub_prios.append(task[key] * val)
            except KeyError:
                self.cease(task, rc=2,
                           msg='Weights cnfg to UDA definition discrepancy.')

        return sum(sub_prios)

    def act(self, task):
        if task['status'] in ['deleted']:
            self.cease(task, msg='Nothing to do.')

        priority = self._calculate(task)
        task['priority'] = priority

        self.cease(task, msg='Prioritization succeeded.')
