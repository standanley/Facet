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

print('\nabove TemplateMaster')

class TemplateMaster(Circuit, metaclass=TemplateKind):

    def required_port_info(self):
        # TODO: this should give more info than just the names of the ports
        return '\n'.join([str(port) for port in self.required_ports])

    # gets called when someone subclasses a template, checks that all of
    # required_ports got mapped to in mapping
    def check_required_ports(self):
        for port_name in self.required_ports:
            assert hasattr(self, port_name), 'Did not associate port %s'%portname

print('\nAfter template master')

class AmpTemplate(TemplateMaster):
    __name__ = 'abc123'
    required_ports = ['in_single', 'out_single']

print('\nAfter AmpTemplate')

class MyAmpInterface(AmpTemplate):
    name = 'MyAmpInterface'
    IO = ['my_in', In(Bit), 'my_out', Out(Bit)]

    def mapping(self):
        self.in_single = self.my_in
        self.out_single = self.my_out

print('\nAfter MyAmpInterface')

class MyAmp1(MyAmpInterface):
    @classmethod
    def definition(io):
        print('doing definition')
        temp = ~io.my_in
        print('temp is' ,temp)
        #io.my_out <= ~io.my_in
        wire(temp, io.my_out)

print('\nAfter MyAmp1')

def test_thing():

    MyAmp1()

    t = fault.Tester(MyAmp1)


    t.poke(MyAmp1.my_in, 0)
    t.eval()
    t.expect(MyAmp1.my_out, 1)

    t.poke(MyAmp1.my_in, 1)
    t.eval()
    t.expect(MyAmp1.my_out, 0)

    print(MyAmp1.in_single)

    # now with template names
    t.poke(MyAmp1.in_single, 0)
    t.eval()
    t.expect(MyAmp1.out_single, 1)

    t.poke(MyAmp1.in_single, 1)
    t.eval()
    t.expect(MyAmp1.out_single, 0)


    t.compile_and_run('verilator')

if __name__ == '__main__':
    test_thing()
