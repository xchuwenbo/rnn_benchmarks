from __future__ import print_function
from platoon.channel import Controller


class LMController(Controller):

    def __init__(self, control_port):
        Controller.__init__(self, control_port)
        self.wps = {}

    def handle_control(self, req, worker_id):
        control_response = ""

        if req == 'done':
            self.worker_is_done(worker_id)
            print("Worker {}: Done training.".format(worker_id))
        elif 'wps' in req:
            print("Worker {}: {} wps for epoch {}.".format(worker_id, req['wps'], req['epoch']))
            wps = self.wps.get(req['epoch'], [])
            wps += [req['wps']]
            self.wps[req['epoch']] = wps

        return control_response

if __name__ == '__main__':
    l = LMController(control_port=5567)
    print("Controller is ready.")
    l.serve()

    print(l.wps)
    for e, w in l.wps:
        print("Epoch {}: {} wps".format(e, w.sum()))
