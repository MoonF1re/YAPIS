# Generated from ListLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ListLangParser import ListLangParser
else:
    from ListLangParser import ListLangParser

# This class defines a complete listener for a parse tree produced by ListLangParser.
class ListLangListener(ParseTreeListener):

    # Enter a parse tree produced by ListLangParser#program.
    def enterProgram(self, ctx:ListLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by ListLangParser#program.
    def exitProgram(self, ctx:ListLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by ListLangParser#functionDecl.
    def enterFunctionDecl(self, ctx:ListLangParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by ListLangParser#functionDecl.
    def exitFunctionDecl(self, ctx:ListLangParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by ListLangParser#parameterList.
    def enterParameterList(self, ctx:ListLangParser.ParameterListContext):
        pass

    # Exit a parse tree produced by ListLangParser#parameterList.
    def exitParameterList(self, ctx:ListLangParser.ParameterListContext):
        pass


    # Enter a parse tree produced by ListLangParser#statement.
    def enterStatement(self, ctx:ListLangParser.StatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#statement.
    def exitStatement(self, ctx:ListLangParser.StatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#assignment.
    def enterAssignment(self, ctx:ListLangParser.AssignmentContext):
        pass

    # Exit a parse tree produced by ListLangParser#assignment.
    def exitAssignment(self, ctx:ListLangParser.AssignmentContext):
        pass


    # Enter a parse tree produced by ListLangParser#returnStatement.
    def enterReturnStatement(self, ctx:ListLangParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#returnStatement.
    def exitReturnStatement(self, ctx:ListLangParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#ifStatement.
    def enterIfStatement(self, ctx:ListLangParser.IfStatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#ifStatement.
    def exitIfStatement(self, ctx:ListLangParser.IfStatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#whileStatement.
    def enterWhileStatement(self, ctx:ListLangParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#whileStatement.
    def exitWhileStatement(self, ctx:ListLangParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#untilStatement.
    def enterUntilStatement(self, ctx:ListLangParser.UntilStatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#untilStatement.
    def exitUntilStatement(self, ctx:ListLangParser.UntilStatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#forStatement.
    def enterForStatement(self, ctx:ListLangParser.ForStatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#forStatement.
    def exitForStatement(self, ctx:ListLangParser.ForStatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#writeStatement.
    def enterWriteStatement(self, ctx:ListLangParser.WriteStatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#writeStatement.
    def exitWriteStatement(self, ctx:ListLangParser.WriteStatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#readStatement.
    def enterReadStatement(self, ctx:ListLangParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by ListLangParser#readStatement.
    def exitReadStatement(self, ctx:ListLangParser.ReadStatementContext):
        pass


    # Enter a parse tree produced by ListLangParser#block.
    def enterBlock(self, ctx:ListLangParser.BlockContext):
        pass

    # Exit a parse tree produced by ListLangParser#block.
    def exitBlock(self, ctx:ListLangParser.BlockContext):
        pass


    # Enter a parse tree produced by ListLangParser#castExpr.
    def enterCastExpr(self, ctx:ListLangParser.CastExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#castExpr.
    def exitCastExpr(self, ctx:ListLangParser.CastExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#inExpr.
    def enterInExpr(self, ctx:ListLangParser.InExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#inExpr.
    def exitInExpr(self, ctx:ListLangParser.InExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#memberExpr.
    def enterMemberExpr(self, ctx:ListLangParser.MemberExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#memberExpr.
    def exitMemberExpr(self, ctx:ListLangParser.MemberExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#orExpr.
    def enterOrExpr(self, ctx:ListLangParser.OrExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#orExpr.
    def exitOrExpr(self, ctx:ListLangParser.OrExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#comparisonExpr.
    def enterComparisonExpr(self, ctx:ListLangParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#comparisonExpr.
    def exitComparisonExpr(self, ctx:ListLangParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:ListLangParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:ListLangParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#parenExpr.
    def enterParenExpr(self, ctx:ListLangParser.ParenExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#parenExpr.
    def exitParenExpr(self, ctx:ListLangParser.ParenExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#indexExpr.
    def enterIndexExpr(self, ctx:ListLangParser.IndexExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#indexExpr.
    def exitIndexExpr(self, ctx:ListLangParser.IndexExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#literalExpr.
    def enterLiteralExpr(self, ctx:ListLangParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#literalExpr.
    def exitLiteralExpr(self, ctx:ListLangParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#functionCallExpr.
    def enterFunctionCallExpr(self, ctx:ListLangParser.FunctionCallExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#functionCallExpr.
    def exitFunctionCallExpr(self, ctx:ListLangParser.FunctionCallExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#listExpr.
    def enterListExpr(self, ctx:ListLangParser.ListExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#listExpr.
    def exitListExpr(self, ctx:ListLangParser.ListExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:ListLangParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:ListLangParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#rangeExpr.
    def enterRangeExpr(self, ctx:ListLangParser.RangeExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#rangeExpr.
    def exitRangeExpr(self, ctx:ListLangParser.RangeExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#idExpr.
    def enterIdExpr(self, ctx:ListLangParser.IdExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#idExpr.
    def exitIdExpr(self, ctx:ListLangParser.IdExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#andExpr.
    def enterAndExpr(self, ctx:ListLangParser.AndExprContext):
        pass

    # Exit a parse tree produced by ListLangParser#andExpr.
    def exitAndExpr(self, ctx:ListLangParser.AndExprContext):
        pass


    # Enter a parse tree produced by ListLangParser#functionCall.
    def enterFunctionCall(self, ctx:ListLangParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by ListLangParser#functionCall.
    def exitFunctionCall(self, ctx:ListLangParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by ListLangParser#argumentList.
    def enterArgumentList(self, ctx:ListLangParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by ListLangParser#argumentList.
    def exitArgumentList(self, ctx:ListLangParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by ListLangParser#expressionList.
    def enterExpressionList(self, ctx:ListLangParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by ListLangParser#expressionList.
    def exitExpressionList(self, ctx:ListLangParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by ListLangParser#type.
    def enterType(self, ctx:ListLangParser.TypeContext):
        pass

    # Exit a parse tree produced by ListLangParser#type.
    def exitType(self, ctx:ListLangParser.TypeContext):
        pass


    # Enter a parse tree produced by ListLangParser#literal.
    def enterLiteral(self, ctx:ListLangParser.LiteralContext):
        pass

    # Exit a parse tree produced by ListLangParser#literal.
    def exitLiteral(self, ctx:ListLangParser.LiteralContext):
        pass



del ListLangParser