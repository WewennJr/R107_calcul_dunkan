import matplotlib.pyplot as plt
import numpy as np

def coef2():
    #listeUE1 = {r101 : 10,r102 : 10,r103 : 7,r104 : 7,r106 : 5,r108 : 6,r110 : 5,r111 : 4,r112 : 2,r113 : 5,r114 : 5,SAE11 : 20,SAE12 : 20,SAE16 : 7}
    #listeUE2 = {r101 : 4,r103 : 2,r104 : 8,r105 : 6,r110 : 5,r111 : 5,r112 : 2,r113 : 9,r114 : 9,r115 : 3,SAE13 : 29,SAE16 : 7}
    #listeUE3 = {r101 : 4,r103 : 2,r106 : 5,r107 : 15,r108 : 0,r109 6 ,r110 : 5,r111 : 5,r112 : 2,r115 : 3,SAE14 : 20,SAE15 : 20,SAE16 : 7}


    r101 = float(input("Quelles notes avez vous obtenu pour la ressources r101 dans votre UE1"))
    r102 = float(input("Quelles notes avez vous obtenu pour la ressources r102 dans votre UE1"))
    r103 = float(input("Quelles notes avez vous obtenu pour la ressources r103 dans votre UE1"))
    r104 = float(input("Quelles notes avez vous obtenu pour la ressources r104 dans votre UE1"))
    r105 = float(input("Quelles notes avez vous obtenu pour la ressources r105 dans votre UE1"))
    r106 = float(input("Quelles notes avez vous obtenu pour la ressources r106 dans votre UE1"))
    r107 = float(input("Quelles notes avez vous obtenu pour la ressources r107 dans votre UE1"))
    r108 = float(input("Quelles notes avez vous obtenu pour la ressources r108 dans votre UE1"))
    r109 = float(input("Quelles notes avez vous obtenu pour la ressources r109 dans votre UE1"))
    r110 = float(input("Quelles notes avez vous obtenu pour la ressources r110 dans votre UE1"))
    r111 = float(input("Quelles notes avez vous obtenu pour la ressources r111 dans votre UE1"))
    r112 = float(input("Quelles notes avez vous obtenu pour la ressources r112 dans votre UE1"))
    r113 = float(input("Quelles notes avez vous obtenu pour la ressources r113 dans votre UE1"))
    r114 = float(input("Quelles notes avez vous obtenu pour la ressources r114 dans votre UE1"))
    r115 = float(input("Quelles notes avez vous obtenu pour la ressources r115 dans votre UE1"))
    SAE11 = float(input("Quelles notes avez vous obtenu pour la ressources SAE11 dans votre UE1"))
    SAE12 = float(input("Quelles notes avez vous obtenu pour la ressources SAE12 dans votre UE1"))
    SAE13 = float(input("Quelles notes avez vous obtenu pour la ressources SAE13 dans votre UE1"))
    SAE14 = float(input("Quelles notes avez vous obtenu pour la ressources SAE14 dans votre UE1"))
    SAE15 = float(input("Quelles notes avez vous obtenu pour la ressources SAE15 dans votre UE1"))
    SAE16 = float(input("Quelles notes avez vous obtenu pour la ressources SAE16 dans votre UE1"))

    1r101 = 11
    1r102 = 11
    1r103 = 15
    1r104 = 15
    1r105 = 15
    1r106 = 13
    1r107 = 13
    1r108 = 9
    1r109 = 9
    1r110 = 18
    1r111 = 5
    1r112 = 6
    1r113 = 10
    1r114 = 10
    1r115 = 10
    1SAE11 = 15
    1SAE12 = 12
    1SAE13 = 9
    1SAE14 = 10
    1SAE15 = 12
    1SAE16 = 18


    1listR = [1r101,1r102,1r103,1r104,1r105,1r106,1r107,1r108,1r109,1r110,1r111,1r112,1r113,1r114,1r115,1SAE11,1SAE12,1SAE13,1SAE14,1SAE15,1SAE16]
    listR = [r101,r102,r103,r104,r105,r106,r107,r108,r109,r110,r111,r112,r113,r114,r115,SAE11,SAE12,SAE13,SAE14,SAE15,SAE16]
    coefUE1 = [10,10,7,7,0,5,0,6,0,5,4,2,5,5,0,20,20,0,0,0,7]
    coefUE2 = [4,0,2,8,6,0,0,0,0,5,5,2,9,9,3,0,0,29,0,0,7]
    coefUE3 = [4,0,2,0,0,5,15,6,4,5,5,2,0,0,3,0,0,0,20,20,7]

    
    S1 = np.average(1listR, weights=coefUE1)
    S2 = np.average(1listR, weights=coefUE2)
    S3 = np.average(1listR, weights=coefUE3)
    S_ALL = [S1,S2,S3]

    test = [0,5,10,15,20]

    plt.style.use("petroff10")
    plt.bar(["Ue1","Ue2","Ue3"], S_ALL, width = 0.5, color='b' )
    plt.title("Diagramme des UE")
    plt.xlabel("UE")
    plt.ylabel("Notes")
    plt.show()
    
            
    print(S1)
    print(S2)
    print(S3)

coef2()

