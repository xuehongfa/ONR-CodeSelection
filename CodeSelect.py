from joern.all import JoernSteps
import glob


def Tran(x):
    switcher ={
        "PrimaryExpression": "$COS",
        "CallExpression": "$CAL",
        "Condition": "$CON",
        "Identifier": "$VAR",
        "CastExpression": "$CAT",
        "OrExpression": "$OP",
        "IncDecOp": "$OP",
        "UnaryOp": "$UOP",
        "AdditiveExpression": "$ADD",
        "ArrayIndexing":"$IDX"
    }
    return switcher.get(x, 'null')

j=JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data/')

# j.addStepsDir('Use this to inject utility traversals')

j.connectToDatabase()

ptrlist=open('/home/hongfa/workspace/thttpd_workspace/ptrList','r')

ptrs=ptrlist.readlines()

for ptr in ptrs:

    #print ptr
    functionID = ptr.split("functionId:")[1]
    nodeID = ptr.split("	")[0]
    print nodeID
    ptrname_query= """g.v("""+nodeID+""").out().astNodes().filter{it.type=="Identifier"}.code"""
    ptrname =  j.runGremlinQuery(ptrname_query)

    statements_query="""g.v("""+functionID+""").out().filter{it.type == "FunctionDef"}.ithChildren("0").astNodes().filter{it.type == "Identifier" && it.code=="""+"\""+ptrname[0]+"\""+"""}.statements()"""
    #res =  j.runCypherQuery('g.v(84).out().filter{it.type=="Identifier"}.code')
    statements =  j.runGremlinQuery(statements_query)
    P_file=open(functionID+ptrname[0],'a')
    #print len(statements)
    statements_list=[]
    for s in statements:


        print s
        s = str(s)
        ID = s.split(" {childNum")[0].split("(n")[1]
        type = s.split("type:")[1].split("\"")[1]
        if ID in statements_list:
            continue
        else:
            statements_list.append(ID)
            #print statements_list
        if type == "IdentifierDeclStatement":

            query = """g.v("""+ID+""").out().out()"""
            depth_2 = j.runGremlinQuery(query)
            #print depth_2
            query2 = """g.v("""+ID+""").out().ithChildren("2")"""
            children_2 = j.runGremlinQuery(query2)

            if len(children_2) == 0:

                #print s
                query = """g.v("""+ID+""").out().astNodes().filter{it.type == "Identifier" && it.code=="""+"\""+ptrname[0]+"\""+"""}"""
                leaf_node = j.runGremlinQuery(query)
                #print IDT[0]
                leaf_id = str(leaf_node[0]).split(" {childNum")[0].split("(n")[1]
                query = """g.v("""+leaf_id+""").parents().ithChildren("0").code"""
                IDT = j.runGremlinQuery(query)
                IDT = str(IDT[0])
                Pattern = IDT + " " + "$ITF"
                P_file.write(Pattern+"\n")


            else:

                query2 = """g.v("""+ID+""").out().ithChildren("2").type"""
                children_2_type = j.runGremlinQuery(query2)
                #print children_2_type

                if str(children_2_type[0]) == "AssignmentExpr":

                    children_2_id = str(children_2[0]).split(" {childNum")[0].split("(n")[1]
                    query = """g.v("""+children_2_id+""").ithChildren("1").type"""
                    assignment_children_2_type = j.runGremlinQuery(query)
                    #print assignment_children_2
                    query = """g.v("""+ID+""").out().astNodes().filter{it.type == "Identifier" && it.code=="""+"\""+ptrname[0]+"\""+"""}"""
                    leaf_node = j.runGremlinQuery(query)
                    #print IDT[0]
                    leaf_id = str(leaf_node[0]).split(" {childNum")[0].split("(n")[1]
                    query = """g.v("""+leaf_id+""").parents().ithChildren("0").code"""
                    IDT = j.runGremlinQuery(query)
                    IDT = str(IDT[0])

                    if Tran(str(assignment_children_2_type[0] ) != "null"):
                        Pattern = IDT+" "+"$ITF"+" "+"$ASG"+" "+Tran(str(assignment_children_2_type[0]))
                        P_file.write(Pattern+"\n")


                if str(children_2_type[0]) == "PrimaryExpression":
                    children_2_id = str(children_2[0]).split(" {childNum")[0].split("(n")[1]
                    query = """g.v("""+children_2_id+""").ithChildren("1").type"""
                    assignment_children_2_type = j.runGremlinQuery(query)
                    #print assignment_children_2
                    query = """g.v("""+ID+""").out().astNodes().filter{it.type == "Identifier" && it.code=="""+"\""+ptrname[0]+"\""+"""}"""
                    leaf_node = j.runGremlinQuery(query)
                    #print IDT[0]
                    leaf_id = str(leaf_node[0]).split(" {childNum")[0].split("(n")[1]
                    query = """g.v("""+leaf_id+""").parents().ithChildren("0").code"""
                    IDT = j.runGremlinQuery(query)
                    IDT = str(IDT[0])
                    Pattern = IDT+" "+"$ITF"
                    P_file.write(Pattern+"\n")

        if type == "ExpressionStatement":


            query = """g.v("""+ID+""").out()"""
            depth_1 = j.runGremlinQuery(query)
            for d in depth_1:

                d = str(d)
                d_type = d.split("type:")[1].split("\"")[1]
                d_ID = d.split(" {childNum")[0].split("(n")[1]
                #print d_type
                if d_type == "AssignmentExpr":

                    children_0 = j.runGremlinQuery("""g.v("""+d_ID+""").ithChildren("0").astNodes().filter{it.type == "Identifier" && it.code=="""+"\""+ptrname[0]+"\""+"""}""")
                    query = """g.v("""+d_ID+""").ithChildren("1")"""
                    children_1 = j.runGremlinQuery(query)
                    #Callee = j.runGremlinQuery(query2)
                    children_1_type = str(children_1[0]).split("type:")[1].split("\"")[1]
                    if len(children_0) > 0 :

                        Pattern = "$ITF" + " " +"$ASG" + " "+ Tran(children_1_type)
                        P_file.write(Pattern+"\n")
                    else:
                        children_0 = j.runGremlinQuery("""g.v("""+d_ID+""").ithChildren("0")""")
                        children_0_type = str(children_0[0]).split("type:")[1].split("\"")[1]
                        Pattern = Tran(children_0_type) + " "+ "$ASG" + " " +  Tran(children_1_type) + " "+"$ITF"
                        P_file.write(Pattern+"\n")

                if d_type == "CallExpression":
                    Pattern = "$CAL"+" "+"$ITF"
                    P_file.write(Pattern+"\n")



        if type == "Condition" :
            Pattern = "$ITF"+" "+"$CMP"+" "+"$COS"
            P_file.write(Pattern+"\n")

        if type == "ForInit":
            Pattern = "$LOP"+" "+"$ITF"
            P_file.write(Pattern+"\n")

        if type == "ReturnStatement":
            Pattern = "$RET" + " "+"$ITF"
            P_file.write(Pattern+"\n")

        if type == "IncDecOp":
            Pattern = "$IDO" +" "+"$ITF"
            P_file.write(Pattern+"\n")






