from magma import *
import mantle
import fault


class TemplateKind(circuit.DefineCircuitKind):


    def __new__(metacls, name, bases, dct):
        cls = super(TemplateKind, metacls).__new__(metacls, name, bases, dct)

        #print('call to __new__', metacls, name, bases, dct, 'cls', cls)

        if name == 'TemplateMaster':
            # no checks are needed
            print('creation of TemplateMaster, returning now')
            return cls

        # TODO we want to differentiate between a template class and a 
        # subclass of a template class. Is this a good way to do it?
        is_template = (TemplateMaster in bases)
        print('new class', name, 'is_template is', is_template)

        if is_template:
            assert hasattr(cls, 'required_ports'), 'Template must give required ports'
            assert not hasattr(cls, 'mapping'), 'mapping is for the instance, not the template'

        else:
            assert hasattr(cls, 'mapping'), 'Subclass of template must provide port mapping'
            print('calling mapping from TemplateKind.__new__')
            # call user's function to associate ports
            cls.mapping(cls)
            # check that all the required ports actually got associated
            cls.check_required_ports(cls)


        return cls

class TemplateMaster(Circuit, metaclass=TemplateKind):

    @classmethod
    def required_port_info(self):
        # TODO: this should give more info than just the names of the ports
        return '\n'.join([str(port) for port in self.required_ports])

    # gets called when someone subclasses a template, checks that all of
    # required_ports got mapped to in mapping
    def check_required_ports(self):
        for port_name in self.required_ports:
            assert hasattr(self, port_name), 'Did not associate port %s'%port_name
