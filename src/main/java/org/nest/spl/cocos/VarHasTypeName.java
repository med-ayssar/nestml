/*
 * Copyright (c)  RWTH Aachen. All rights reserved.
 *
 * http://www.se-rwth.de/
 */
package org.nest.spl.cocos;

import de.monticore.cocos.CoCoLog;
import de.monticore.symboltable.Scope;
import org.nest.spl._ast.ASTDeclaration;
import org.nest.spl._cocos.SPLASTDeclarationCoCo;
import org.nest.symboltable.symbols.NESTMLTypeSymbol;

import java.util.Optional;

import static com.google.common.base.Preconditions.checkArgument;

/**
 * Checks that the variable name is not a type name, e.g. integer integer = 1.
 *
 * @author (last commit) $$Author$$
 * @version $$Revision$$, $$Date$$
 * @since 0.0.1
 */
public class VarHasTypeName implements SPLASTDeclarationCoCo {
  public static final String ERROR_CODE = "SPL_VARIABLE_HAS_TYPE_NAME";
  private static final String ERROR_MSG_FORMAT = "Variable '%s' cannot have the same name as a type.";

  @Override
  public void check(final ASTDeclaration astDeclaration) {
    checkArgument(astDeclaration.getEnclosingScope().isPresent(), "Declaration hast no scope. Run symboltable creator.");
    final Scope scope = astDeclaration.getEnclosingScope().get();

    for (String var : astDeclaration.getVars()) {
      // tries to resolve the variable name as type. if it is possible, then the variable name clashes with type name is reported as an error
      final Optional<NESTMLTypeSymbol> res = scope.resolve(var, NESTMLTypeSymbol.KIND);

      // could resolve type as variable, report an error
      if (res.isPresent()) {
        CoCoLog.error(
            ERROR_CODE,
            String.format(ERROR_MSG_FORMAT, var),
            astDeclaration.get_SourcePositionEnd());
      }

    }

  }

}
