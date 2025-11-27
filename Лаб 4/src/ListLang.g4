grammar ListLang;

// Парсерные правила
program: (functionDecl | statement)* EOF;

functionDecl: 'function' ID '(' parameterList? ')' block;

parameterList: ID (',' ID)*;

statement: 
    assignment ';'
    | functionCall ';' 
    | returnStatement ';'
    | ifStatement
    | whileStatement
    | untilStatement
    | forStatement
    | writeStatement ';'
    | readStatement ';'
    | block
    | expression ';'
    ;

assignment: ID '=' expression;

returnStatement: 'return' expression?;

ifStatement: 'if' expression block ('else' block)?;

whileStatement: 'while' expression block;

untilStatement: 'until' expression block;

forStatement: 'for' assignment 'to' expression block;

writeStatement: 'write' '(' expression ')';

readStatement: 'read' '(' ')';

block: '{' statement* '}';

expression:
    literal                                    #literalExpr
    | ID                                       #idExpr
    | functionCall                             #functionCallExpr
    | '(' expression ')'                       #parenExpr
    | '[' expressionList? ']'                  #listExpr
    | expression '[' expression ']'            #indexExpr
    | expression '.' ID                        #memberExpr
    | '(' type ')' expression                  #castExpr
    | expression op=('*' | '/' | '%') expression #multiplicativeExpr
    | expression op=('+' | '-') expression     #additiveExpr
    | expression '..' expression               #rangeExpr
    | expression IN expression                 #inExpr
    | expression op=('<' | '>' | '<=' | '>=' | '==' | '!=') expression #comparisonExpr
    | expression '&&' expression               #andExpr
    | expression '||' expression               #orExpr
    ;

functionCall: ID '(' argumentList? ')';

argumentList: expression (',' expression)*;

expressionList: expression (',' expression)*;

type: 'int' | 'float' | 'element' | 'list' | 'tree' | 'queue';

literal: 
    INT
    | FLOAT
    | STRING
    | 'true'
    | 'false'
    | 'null'
    ;

// Лексерные правила
// Ключевые слова
FUNCTION: 'function';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
UNTIL: 'until';
FOR: 'for';
RETURN: 'return';
TO: 'to';
IN: 'in';  // Объединяем IN и IN_OP в один токен
WRITE: 'write';
READ: 'read';

// Типы
INT_TYPE: 'int';
FLOAT_TYPE: 'float';
ELEMENT: 'element';
LIST: 'list';
TREE: 'tree';
QUEUE: 'queue';

// Литералы
TRUE: 'true';
FALSE: 'false';
NULL: 'null';

// Операторы и разделители
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
MOD: '%';
ASSIGN: '=';
RANGE: '..';
LT: '<';
GT: '>';
LTE: '<=';
GTE: '>=';
EQ: '==';
NEQ: '!=';
AND: '&&';
OR: '||';
LPAREN: '(';
RPAREN: ')';
LBRACK: '[';
RBRACK: ']';
LBRACE: '{';
RBRACE: '}';
DOT: '.';
COMMA: ',';
SEMI: ';';

// Идентификаторы и литералы
ID: [a-zA-Z_][a-zA-Z_0-9]*;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]* | '.' [0-9]+;
STRING: '"' (~["\\] | '\\' .)* '"';

// Пропускаемые символы
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;