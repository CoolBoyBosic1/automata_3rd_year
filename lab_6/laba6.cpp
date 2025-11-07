#include <clang-c/Index.h>
#include <iostream>
#include <vector>

struct BreakableNode {
    bool is_loop;   
    bool has_break; 
};

struct VisitContext {
    std::vector<BreakableNode> nodes;
    std::vector<int> breakable_stack;
};

void traverse(CXCursor cursor, VisitContext* ctx);

CXChildVisitResult visitor(CXCursor c, CXCursor parent, CXClientData client_data) {
    auto* ctx = static_cast<VisitContext*>(client_data);
    traverse(c, ctx);
    return CXChildVisit_Continue;
}

void traverse(CXCursor cursor, VisitContext* ctx) {
    CXCursorKind kind = clang_getCursorKind(cursor);

    if (kind == CXCursor_TranslationUnit) {
        clang_visitChildren(cursor, visitor, ctx);
        return;
    }

    CXSourceLocation loc = clang_getCursorLocation(cursor);
    if (!clang_Location_isFromMainFile(loc)) {
        return; 
    }

    if (kind == CXCursor_ForStmt ||
        kind == CXCursor_WhileStmt ||
        kind == CXCursor_DoStmt ||
        kind == CXCursor_CXXForRangeStmt) {

        BreakableNode node;
        node.is_loop = true;
        node.has_break = false;

        ctx->nodes.push_back(node);
        int idx = static_cast<int>(ctx->nodes.size()) - 1;

        ctx->breakable_stack.push_back(idx);
        clang_visitChildren(cursor, visitor, ctx);
        ctx->breakable_stack.pop_back();
        return;
    }

    if (kind == CXCursor_SwitchStmt) {
        BreakableNode node;
        node.is_loop = false;
        node.has_break = false;

        ctx->nodes.push_back(node);
        int idx = static_cast<int>(ctx->nodes.size()) - 1;

        ctx->breakable_stack.push_back(idx);
        clang_visitChildren(cursor, visitor, ctx);
        ctx->breakable_stack.pop_back();
        return;
    }

    if (kind == CXCursor_BreakStmt) {
        if (!ctx->breakable_stack.empty()) {
            int top = ctx->breakable_stack.back();
            ctx->nodes[top].has_break = true;
        }
        return;
    }

    clang_visitChildren(cursor, visitor, ctx);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Використання: " << argv[0] << " <cpp-файл>\n";
        return 1;
    }

    const char* filename = argv[1];

    CXIndex index = clang_createIndex(0, 0);

    const char* args[] = {
        "-std=c++17"
    };

    CXTranslationUnit tu = clang_parseTranslationUnit(
        index,
        filename,
        args, 1,         
        nullptr, 0,       
        CXTranslationUnit_None
    );

    if (tu == nullptr) {
        std::cerr << "Не вдалося створити TranslationUnit для файлу: " << filename << "\n";
        clang_disposeIndex(index);
        return 1;
    }

    CXCursor rootCursor = clang_getTranslationUnitCursor(tu);

    VisitContext ctx;
    traverse(rootCursor, &ctx);

    int loops_with_break = 0;
    for (const auto& node : ctx.nodes) {
        if (node.is_loop && node.has_break) {
            ++loops_with_break;
        }
    }

    std::cout << "Кількість циклів, що можуть завершуватись за інструкцією break: "
              << loops_with_break << std::endl;

    clang_disposeTranslationUnit(tu);
    clang_disposeIndex(index);

    return 0;
}
