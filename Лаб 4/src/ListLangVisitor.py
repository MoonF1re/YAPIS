# Generated from ListLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ListLangParser import ListLangParser
else:
    from ListLangParser import ListLangParser

# This class defines a complete generic visitor for a parse tree produced by ListLangParser.

class ListLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ListLangParser#program.
    def visitProgram(self, ctx:ListLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#functionDecl.
    def visitFunctionDecl(self, ctx:ListLangParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#parameterList.
    def visitParameterList(self, ctx:ListLangParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#statement.
    def visitStatement(self, ctx:ListLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#assignment.
    def visitAssignment(self, ctx:ListLangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#returnStatement.
    def visitReturnStatement(self, ctx:ListLangParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#ifStatement.
    def visitIfStatement(self, ctx:ListLangParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#whileStatement.
    def visitWhileStatement(self, ctx:ListLangParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#untilStatement.
    def visitUntilStatement(self, ctx:ListLangParser.UntilStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#forStatement.
    def visitForStatement(self, ctx:ListLangParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#writeStatement.
    def visitWriteStatement(self, ctx:ListLangParser.WriteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#readStatement.
    def visitReadStatement(self, ctx:ListLangParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#block.
    def visitBlock(self, ctx:ListLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#castExpr.
    def visitCastExpr(self, ctx:ListLangParser.CastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#inExpr.
    def visitInExpr(self, ctx:ListLangParser.InExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#memberExpr.
    def visitMemberExpr(self, ctx:ListLangParser.MemberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#orExpr.
    def visitOrExpr(self, ctx:ListLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#comparisonExpr.
    def visitComparisonExpr(self, ctx:ListLangParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:ListLangParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#parenExpr.
    def visitParenExpr(self, ctx:ListLangParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#indexExpr.
    def visitIndexExpr(self, ctx:ListLangParser.IndexExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#literalExpr.
    def visitLiteralExpr(self, ctx:ListLangParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#functionCallExpr.
    def visitFunctionCallExpr(self, ctx:ListLangParser.FunctionCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#listExpr.
    def visitListExpr(self, ctx:ListLangParser.ListExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:ListLangParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#rangeExpr.
    def visitRangeExpr(self, ctx:ListLangParser.RangeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#idExpr.
    def visitIdExpr(self, ctx:ListLangParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#andExpr.
    def visitAndExpr(self, ctx:ListLangParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#functionCall.
    def visitFunctionCall(self, ctx:ListLangParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#argumentList.
    def visitArgumentList(self, ctx:ListLangParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#expressionList.
    def visitExpressionList(self, ctx:ListLangParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#type.
    def visitType(self, ctx:ListLangParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ListLangParser#literal.
    def visitLiteral(self, ctx:ListLangParser.LiteralContext):
        return self.visitChildren(ctx)



del ListLangParser