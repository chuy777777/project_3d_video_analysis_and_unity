using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using MyNamespace;
using Algorithms;

public class HandsModel : MonoBehaviour
{
    [SerializeField] 
    public string handType="";
    public List<GameObject> jointFatherGameObjectsList;

    void Start()
    {
        List<Transform> jointTransformsList=new List<Transform>();
        MyNamespace.Functions.TransformsByPatternRecursiveTransform(transformsList: jointTransformsList, rootTransform: this.gameObject.transform, pattern: @"joint_\d+");
        MyNamespace.Functions.OrderByNameTransformsList(transformsList: jointTransformsList);
        this.jointFatherGameObjectsList=MyNamespace.Functions.CreateFathersWithSpecificOrientation(creationCoordinateSystemList: Algorithms.AlgorithmMediaPipeHands.creationCoordinateSystemList, jointTransformsList: jointTransformsList);
    }

    void Update()
    {
        this.Move(algorithmMediaPipeHands: SocketClient.instance.algorithmMediaPipeHands);
    }

    public void Move(Algorithms.AlgorithmMediaPipeHands algorithmMediaPipeHands)
    {
        if(this.handType == "Left" && algorithmMediaPipeHands.points3DULeftList != null && algorithmMediaPipeHands.eulerAnglesMLeftList != null)
        {
            List<Vector3> points3DULeftList=algorithmMediaPipeHands.points3DULeftList;
            List<Vector3> eulerAnglesMLeftList=algorithmMediaPipeHands.eulerAnglesMLeftList;

            MyNamespace.Functions.MakeRotations(gameObjectsList: this.jointFatherGameObjectsList, eulerAnglesMList: eulerAnglesMLeftList);
        }
        if(this.handType == "Right" && algorithmMediaPipeHands.points3DURightList != null && algorithmMediaPipeHands.eulerAnglesMRightList != null)
        {
            List<Vector3> points3DURightList=algorithmMediaPipeHands.points3DURightList;
            List<Vector3> eulerAnglesMRightList=algorithmMediaPipeHands.eulerAnglesMRightList;

            MyNamespace.Functions.MakeRotations(gameObjectsList: this.jointFatherGameObjectsList, eulerAnglesMList: eulerAnglesMRightList);
        }
    }
}
