using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using MyNamespace;
using Algorithms;

public class PoseModel : MonoBehaviour
{
    public List<GameObject> jointFatherGameObjectsList;

    void Start()
    {
        List<Transform> jointTransformsList=new List<Transform>();
        MyNamespace.Functions.TransformsByPatternRecursiveTransform(transformsList: jointTransformsList, rootTransform: this.gameObject.transform, pattern: @"joint_\d+");
        MyNamespace.Functions.OrderByNameTransformsList(transformsList: jointTransformsList);
        this.jointFatherGameObjectsList=MyNamespace.Functions.CreateFathersWithSpecificOrientation(creationCoordinateSystemList: Algorithms.AlgorithmMediaPipePose.creationCoordinateSystemList, jointTransformsList: jointTransformsList);
    }

    void Update()
    {
        this.Move(algorithmMediaPipePose: SocketClient.instance.algorithmMediaPipePose);
    }

    public void Move(Algorithms.AlgorithmMediaPipePose algorithmMediaPipePose)
    {
        if(algorithmMediaPipePose.points3DUAllList != null && algorithmMediaPipePose.eulerAnglesMAllList != null)
        {
            List<Vector3> points3DUAllList=algorithmMediaPipePose.points3DUAllList;
            List<Vector3> eulerAnglesMAllList=algorithmMediaPipePose.eulerAnglesMAllList;

            MyNamespace.Functions.MakeRotations(gameObjectsList: this.jointFatherGameObjectsList, eulerAnglesMList: eulerAnglesMAllList);
        }
    }
}
