import math
class Calculator:
    class stack:
        class node:
            def __init__(self, val, nextNode):
                self.value = val
                self.next = nextNode
 
        def __init__(self):
            self.top = self.last =  None
            self.size = 0
        def __len__(self):
            return self.size
        def push(self, val):
            newNode = Calculator.stack.node(val, None)
            if self.size == 0:
                self.top = newNode
                self.last = newNode
            else:
                newNode.next = self.top
                self.top = newNode
            self.size += 1
        def pop(self):
            if self.size > 0:
                val = self.top.value
                self.top = self.top.next
                self.size -= 1
                return val
            else:
                return None

    ### Copy from HW4
    def exeOpr(self, num1, opr, num2):
        if opr=="+":
            return num1+num2
        elif opr=="-":
            return num1-num2
        elif opr=="*":
            return num1*num2
        elif opr=="/":
            if num2==0:
                print("zero division error: exeOpr")
                return "zero division error: exeOpr"
            else:
                return num1/num2
        elif opr=="^":
            return num1 ** num2
        else:
            print("fatal internal error in exeOpr")
            return "fatal internal error in exeOpr"

    def findNextOpr(self, s):
        if len(s)<=0 or not isinstance(s,str):
            print("type mimatch error: findNextOpr")
            return "type mimatch error: findNextOpr"
        operators = ['+', '-', '*', '/', '^']
        s = list(s)
        for i in range(len(s)):
            if s[i] in operators:
                return i
        return -1

    def isNumber(self, s):
        if len(s)==0 or not isinstance(s, str):
            print("type mismatch error: isNumber")
            return "type mismatch error: isNumber"
        try:
            s = float(s)
            return True
        except ValueError:
            return False

    def isVariable(self, s):
        if not s[0].isalpha():
            return False
        else:
            for i in s[1:]:
                if not i.isalpha() and not self.isNumber(i):
                    return False
            return True

    def getNextItem(self, expr, pos):
        if len(expr)==0 or not isinstance(expr, str) or pos<0 or pos>=len(expr) or not isinstance(pos, int):
            #print("type mismatch error: getNextItem")
            return None, None, "type mismatch error: getNextItem"
        operators = ['+', '-', '*', '/', '^']

        expr = ''.join(expr.split())
    
        listexpr = list(expr)
    
        try:
            listexpr.remove('')
        except:
            pass
    
        nextNum = ''
    
        for a in range(pos, len(listexpr)):
            if a > 0:
                if listexpr[a].isalpha() or self.isNumber(listexpr[a]) or listexpr[a] == '.' or (listexpr[a] == '-' and listexpr[a - 1] in operators) or\
                ((listexpr[a] == '+' or listexpr[a] == '-') and listexpr[a - 1] == 'e'):
                    nextNum += listexpr[a]
                else:
                    a -= 1
                    break
            else:
                if listexpr[a].isalpha() or self.isNumber(listexpr[a]) or listexpr[a] == '-' or listexpr[a] == '.':
                    nextNum += listexpr[a]
        
    
        if nextNum != '':
            if not self.isVariable(nextNum):
                try:
                    nextNum = float(nextNum)
                except ValueError:
                    pass
        elif nextNum == '':
            nextNum = None


        posNextOp = self.findNextOpr(expr[a:])
        if posNextOp == -1:
            posNextOp = None
            nextOp = None
        else:
            nextOp = expr[a:][posNextOp]
            posNextOp += a

        return nextNum, nextOp, posNextOp
        
    ###functions to change the class instance
    def __init__(self):
        self.lines = []
        self.varDic = {}
        self.functDef='''
        sqrt x: math.sqrt(x) ;
        exp  x: math.exp(x) ;
        sin  x: math.sin(x) ;
        cos  x: math.cos(x) ;
        tan  x: math.tan(x) ;
        ln   x: math.log(x) ;
        lg   x: math.log(x) / math.log(2) ;
        round x, y: x – y * math.floor(x/y)
        '''
        self.functDic={}
        self.setFunct()

    def addStars(self, s):
        s = s.strip()
    
        ret = ''
        if 'return' in s:
            ret = 'return '
            s = s[6:]
        
        #print(s)
        #locate any function name
        startLoc = -1
        endLoc = -1
        locs = []
        lens = []

        for i in self.functDic:
            if i in s:
                locs.append(s.find(i))
                lens.append(len(i))

        if len(locs) > 0:
            first = min(locs)
            ind = locs.index(first)
            length = lens[ind]
            startLoc = first
            endLoc = startLoc + length - 1

        #now we have the start and end location of the first function in the string
            
                
        #now find any two things of interest
        currentThing = None
        nextThing = None
        
        if s == '':
            return s
        else:
            for i in range(len(s)):
                if s[i] != ' ':
                    currentThing = s[i]
                    break
            if currentThing is not None:
                for j in range(i + 1, len(s)):
                    if s[j] != ' ':
                        nextThing = s[j]
                        break
            else:
                return ret + s.strip()

            if nextThing is not None:
                #print('i', i, 'j', j)
                #print(currentThing, nextThing)
                if currentThing.isdigit() or currentThing.isalpha():
                    if nextThing.isdigit() or nextThing.isalpha():
                        if j == startLoc:
                            return ret + s[ : i] + currentThing + '*' + s[startLoc : endLoc + 1] + self.addStars(s[endLoc + 1 : ])
                        
                        elif i == startLoc:
                            return ret + s[: i] + s[startLoc : endLoc + 1] + self.addStars(s[endLoc + 1 :])
                        
                        elif j > i + 1:
                            return ret + s[ : i] + currentThing + '*'  + self.addStars(s[j  : ])
                        
                        elif j == i + 1:
                            if currentThing.isdigit() and nextThing.isalpha():
                                return ret + s[: i + 1] + '*' + self.addStars(s[j : ])
                            else:
                                return ret + s[ : j] + self.addStars(s[j : ])
                        
                        else:
                            return ret + s[ : j ] + self.addStars(s[j : ])

                    elif nextThing == '(':
                        return ret + s[ : i] + currentThing + '*' + self.addStars(s[j : ])
                    
                    else:
                        return ret + s [ : j ] + self.addStars(s[j : ])

                elif currentThing == ')':
                    if nextThing.isalpha() or nextThing.isdigit() or nextThing == '(':
                        return ret + s[ : i] + currentThing + '*' + self.addStars(s[j : ])

                    else:
                        return ret + s[ : j] + self.addStars(s[j : ])

                
                else:
                    return ret + s [ : j ] + self.addStars(s[j : ])
                
            else:
                return ret + s.strip()

            
    # copy from HW4
    def getLines(self, expr):
        for hey in expr.split(';'):
            self.lines.append(hey.split('='))
            
        for a in range(len(self.lines)):
            for b in range(len(self.lines[a])):
                #print(self.lines[a][b])
                self.lines[a][b] = self.addStars(self.lines[a][b]).strip()
                #print(self.lines[a][b])
            
    def _calc(self, expr):
        if len(expr)<=0 or not isinstance(expr,str):
            print("argument error: line A in eval_expr")        
            return "argument error: line A in eval_expr"
        operators = ['+', '-', '*', '/', '^']
    
        expr = expr.strip()
        
        mulLastOpr = None
    
        expr = ''.join(expr.split())
        
        negExpStart = False
    
        if expr[0] == '+' or expr[0] == '*' or expr[0] == '/' or expr[0] == '^':
            return 'error: operator at start'
        elif expr[0] != '-':
            newNumber, newOpr, oprPos = self.getNextItem(expr, 0)
            if self.isVariable(str(newNumber)):
                try:
                    expr = expr.replace(str(newNumber), str(self.varDic[str(newNumber)]))
                except:
                    return 'Error: unbound variable'
                newNumber, newOpr, oprPos = self.getNextItem(expr, 0)
        else:
            newNumber, newOpr, oprPos = self.getNextItem(expr, 1)
            if self.isVariable(str(newNumber)):
                try:
                    expr = expr.replace(str(newNumber), str(self.varDic[str(newNumber)]))
                except:
                    return 'Error: unbound variable'
                newNumber, newOpr, oprPos = self.getNextItem(expr, 1)
            if newOpr == '^':
                negExpStart = True
            else:
                newNumber *= -1
        if newNumber is None:
            print("input formula error: line B in eval_expr")   #Line B
            return "input formula error: line B in eval_expr"
        elif newNumber == 'Error: undefined function':
            return newNumber
        elif newOpr is None:
            return newNumber
        elif newOpr=="+" or newOpr=="-":
            mode="add"
            addResult=newNumber     
            mulResult=None          
            expResult = 0
        elif newOpr=="*" or newOpr=="/":
            mode="mul"
            addResult=0
            mulResult=newNumber
            expResult = 0
            mulLastOpr = newOpr
        elif newOpr == '^':
            mode = 'exp'
            addResult = 0
            mulResult = 0
            expResult = newNumber
        addLastOpr = '+'
        pos=oprPos+1                
        opr=newOpr                  
        while True:
            nextNum, nextOp, nextOpPos = self.getNextItem(expr, pos)
            
            if self.isVariable(str(nextNum)):
                try:
                    expr = expr.replace(str(nextNum), str(self.varDic[str(nextNum)]))
                except:
                    return 'Error: unbound variable'
                
                nextNum, nextOp, nextOpPos = self.getNextItem(expr, pos)

            if nextNum is None:
                return 'error: operator at the end'

            elif nextNum == 'Error: undefined function':
                return nextNum
            
            elif nextOp is None and mode == 'add':
                return self.exeOpr(addResult, opr, nextNum)
            
            elif nextOp is None and mode == 'mul':
                mulResult = self.exeOpr(mulResult, opr, nextNum)
                return self.exeOpr(addResult, addLastOpr, mulResult)
            
            elif nextOp is None and mode == 'exp':
                expResult = self.exeOpr(expResult, opr, nextNum)
                if negExpStart:
                    expResult *= -1
                if mulLastOpr is not None:
                    mulResult = self.exeOpr(mulResult, mulLastOpr, expResult)
                    return self.exeOpr(addResult, addLastOpr, mulResult)
                elif addLastOpr is not None:
                    return self.exeOpr(addResult, addLastOpr, expResult)

            elif (nextOp == '+' or nextOp == '-') and mode == 'add':
                addResult = self.exeOpr(addResult, opr, nextNum)

            elif (nextOp == '+' or nextOp == '-') and mode == 'mul':
                mulResult = self.exeOpr(mulResult, opr, nextNum)
                addResult = self.exeOpr(addResult, addLastOpr, mulResult)
                mulResult = None
                mulLastOpr = None
                mode = 'add'

            elif (nextOp == '+' or nextOp == '-') and mode == 'exp':
                expResult **= nextNum
                if negExpStart:
                    expResult *= -1
                    negExpStart = False
                if mulLastOpr is not None:
                    mulResult = self.exeOpr(mulResult, mulLastOpr, expResult)
                    addResult = self.exeOpr(addResult, addLastOpr, mulResult)
                else:
                    addResult = self.exeOpr(addResult, addLastOpr, expResult)
                mulLastOpr = None
                mode = 'add'

            elif (nextOp == '*' or nextOp == '/') and mode == 'add':
                mulResult = nextNum
                addLastOpr = opr
                mode = 'mul'

            elif (nextOp == '*' or nextOp == '/') and mode == 'mul':
                mulResult = self.exeOpr(mulResult, opr, nextNum)

            elif (nextOp == '*' or nextOp == '/') and mode == 'exp':
                expResult **= nextNum
                if negExpStart:
                    expResult *= -1
                    negExpStart = False
                if mulLastOpr is not None:
                    mulResult = self.exeOpr(mulResult, mulLastOpr, expResult)
                elif addLastOpr is not None:
                    mulResult = expResult
                mulLastOpr = nextOp
                mode = 'mul'

            elif nextOp == '^' and mode == 'add':
                expResult = nextNum
                if nextNum < 0:
                    expResult *= -1
                    negExpStart = True
                addLastOpr = opr
                mode = 'exp'

            elif nextOp == '^' and mode == 'mul':
                expResult = nextNum
                mulLastOpr = opr
                mode = 'exp'
            
            pos = nextOpPos + 1
            opr = nextOp


# new functions
    # from the expression tree exercise
    def mask(self, s):
        nestLevel = 0
        masked = list(s)
        for i in range(len(s)):
            if s[i]==")":
                nestLevel -=1
            elif s[i]=="(":
                nestLevel += 1
            if nestLevel>0 and not (s[i]=="(" and nestLevel==1):  # Line A
                masked[i]=" "
        return "".join(masked)

    def findFunctParen(self,expr):
        # expr = arithmetic expression without a space
        # Find a minimal substring including a function name
        #   and the matched pair of parentheses
        # Return
        #   1st value = the start position of the substring, or None if N/A
        #   2nd value = the end position of the substring, or None if N/A
        #   3rd value = function name, or None if N/A
        #
        # e.g.
        #   s = "2*sin(2*pi)"  -->  returns 2, 10, “sin”
        #   s = "2*32*(2*pi)"  -->  returns 5, 10, None
        #   s = "2*32/8/4/2"   -->  returns None, None, None
        #
        functStr = None
        leftPos = None
        rightPos = None
        newStr = ''
        lol = self.stack()

        for a in range(len(expr)):
            if expr[a].isalpha():
                newStr += expr[a]
                if newStr in self.functDic:
                    functStr = newStr
                    break
            else:
                newStr = ''
 
        if functStr is not None:
            pos = expr.find(functStr)
            leftPos = pos
            pos += (len(functStr) - 1)
            
            for a in range(pos, len(expr)):
                if expr[a] == '(':
                    lol.push(a)
                elif expr[a] == ')':
                    lol.pop()
                    if lol.size == 0:
                        rightPos = a
                        break

        else:
            for a in range(len(expr)):
                if expr[a] == '(':
                    lol.push(a)
                elif expr[a] == ')':
                    leftPar = lol.pop()
                    if lol.size == 0:
                        leftPos = leftPar
                        rightPos = a
                    
        return leftPos, rightPos, functStr


    def setFunct(self):
        self.functDic = {'sqrt': 'math.sqrt(x)', 'exp': 'math.exp(x)', 'sin': 'math.sin(x)',
           'cos': 'math.cos(x)', 'tan': 'math.tan(x)', 'ln': 'math.log(x)',
           'lg': 'math.log(x) / math.log(2)', 'round': 'round(x, d)', 'mod': 'x - y * math.floor(x/y)'}



    # Modify _calcHW3 into:      
    def _calcFunctExpr(self, expr):
        # This allows use of pre-defined functions in one line
        #   returning the calculated value if expr is error-free
        # e.g. expr = 5 / lg ( 2* pi ) 
        #
        # tips:
        #   - remove spaces from expr first
        #   - use findFunctParen
        #   - make recursive calls to calculate the inside parentheses
        #       (or you can use a stack as HW4)
        #   - use exec() or eval() to evaluate a built-in function
        #       with parentheses
        #   - handle two parameters of the round function correctly
        #
        left, right, wtf = self.findFunctParen(expr)

        if wtf is not None:
            weirdString = self.functDic[wtf]
            if wtf != 'round' and wtf != 'mod':
                inPar = self._calcFunctExpr(expr[left + len(wtf) + 1 : right])
                if inPar == 'Error: unbound variable':
                    return inPar
                weirdString = weirdString.replace('(x)', '(' + str(inPar) + ')')
            elif wtf == 'round':
                inPar = expr[left + len(wtf) + 1 : right]
                inPar = inPar.split(',')
                x = self._calcFunctExpr(inPar[0])
                if x == 'Error: unbound variable':
                    return x
                
                d = inPar[1]
                if d == 'Error: unbound variable':
                    return d
                elif int(float(d)) != float(d):
                    return 'Error: cannot round to a float value'
                weirdString = weirdString.replace('(x, d)', '(' + str(x) + ', ' + str(d) + ')')
            elif wtf == 'mod':
                inPar = expr[left + len(wtf) + 1 : right]
                inPar = inPar.split(',')
                x = self._calcFunctExpr(inPar[0])
                y = self._calcFunctExpr(inPar[1])
                if 'Error: unbound variable' in [x, y]:
                    return 'Error: unbound variable'
                weirdString = weirdString.replace('x', str(x))
                weirdString = weirdString.replace('y', str(y))
            try:
                answer = eval(weirdString)
            except ValueError:
                if wtf == 'sqrt':
                    return 'Error: cannot take square root of negative'
                elif wtf == 'lg' or wtf == 'ln':
                    return 'Error: cannot take log of negative'
            except NameError:
                return 'Error: mismatched parentheses'

            try:
                newExpr = expr[:left] + str(answer) + expr[right + 1 :]
            except TypeError:
                return 'Error: mismatched parentheses'
            return self._calcFunctExpr(newExpr)
        
        expr = expr.strip()
        parens = self.stack()
        loc = 0
        while loc < len(expr):
            if expr[loc] == '(':
                parens.push(loc)
            elif expr[loc] == ')':
                start = parens.pop()
                if start is None:
                    return 'Error: mismatched parentheses'
                expr = expr[:start] + str(self._calc(expr[start + 1 : loc])) + expr[loc + 1 : ]
                return self._calcFunctExpr(expr)
            loc += 1
        if parens.size > 0:
            return 'Error: mismtched parentheses'
        return self._calc(expr)




    # Almost or exactly the same as HW4
    def calc(self, expr):
        self.getLines(expr)
        for a in self.lines:
            if 'return' in a[0]:
                self.varDic['__return__'] = self._calcFunctExpr(a[0][6:].strip())
            elif len(a) == 2:
                self.varDic[a[0]] = self._calcFunctExpr(a[1])
                if self.varDic[a[0]] == 'Error: unbound variable':
                    self.varDic['__return__'] = 'Error: unbound variable'
                    break
                elif self.varDic[a[0]] == 'Error: cannot round to a float value':
                    self.varDic['__return__'] = 'Error: cannot round to a float value'
                    break
                elif self.varDic[a[0]] == 'Error: mismatched parentheses':
                    self.varDic['__return__'] = 'Error: mismatched parentheses'
                    break
        try:
            return self.varDic['__return__']
        except:
            return 'Error: no return statement'

c = Calculator()
print(c.calc("pi = 3.14159265; var1 = cos(5pi); var2 = exp(var1); return var1 + sqrt(var2)"))

print(c.calc("return lg(1000)"))
