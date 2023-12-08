class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_variable(self, name, data_type):
        if name in self.symbols:
            raise Exception(f"Erro semântico: Variável '{name}' já declarada.")
        self.symbols[name] = data_type

    def get_variable_type(self, name):
        return self.symbols.get(name, None)


class Semantico:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if hasattr(node, 'children'):
            for child in node.children:
                self.visit(child)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDeclaration(self, node):
        data_type = node.type_spec.value
        for variable in node.variables:
            self.symbol_table.add_variable(variable.value, data_type)

    def visit_Assignment(self, node):
        var_name = node.variable.value
        var_type = self.symbol_table.get_variable_type(var_name)
        if var_type is None:
            raise Exception(f"Erro semântico: Variável '{var_name}' não declarada.")

        expr_type = self.visit(node.expression)
        if var_type != expr_type:
            raise Exception(f"Erro semântico: Atribuição inválida para variável '{var_name}'.")

    def visit_BinOp(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if node.op.type in {'PLUS', 'MINUS', 'TIMES', 'DIVIDE'}:
            if left_type == right_type == 'INTEGER':
                return 'INTEGER'
            else:
                raise Exception("Erro semântico: Operação aritmética inválida.")

    def visit_Num(self, node):
        return 'INTEGER'