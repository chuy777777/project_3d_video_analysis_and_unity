using System.Collections;
using System.Collections.Generic;
using System.Text; 
using System;
using UnityEngine;
using System.Text.RegularExpressions;

namespace MyNamespace
{
    public static class Functions
    {
        public static Vector3 EulerAnglesMFromToRotationMatrix(Vector3 c1, Vector3 c2, Vector3 c3)
        {
            // R=RzRyRx
            float R11 = c1.x, R21 = c1.y, R31 = c1.z;
            float R12 = c2.x, R22 = c2.y, R32 = c2.z;
            float R13 = c3.x, R23 = c3.y, R33 = c3.z;
            Vector3 eulerAnglesM = Vector3.zero;
            if (R31 != -1 && R31 != 1)
            {
                double theta1 = -Math.Asin(R31);
                double theta2 = Math.PI - theta1;
                double psi1 = Math.Atan2(R32 / Math.Cos(theta1), R33 / Math.Cos(theta1));
                double psi2 = Math.Atan2(R32 / Math.Cos(theta2), R33 / Math.Cos(theta2));
                double phi1 = Math.Atan2(R21 / Math.Cos(theta1), R11 / Math.Cos(theta1));
                double phi2 = Math.Atan2(R21 / Math.Cos(theta2), R11 / Math.Cos(theta2));
                eulerAnglesM = new Vector3((float)psi1, (float)theta1, (float)phi1);
            }
            else
            {
                if (R31 == -1)
                {
                    double theta = Math.PI / 2;
                    double phi = 0;
                    double psi = Math.Atan2(R12, R13) + phi;
                    eulerAnglesM = new Vector3((float)psi, (float)theta, (float)phi);
                }
                else
                {
                    double theta = -Math.PI / 2;
                    double phi = 0;
                    double psi = Math.Atan2(-R12, -R13) - phi;
                    eulerAnglesM = new Vector3((float)psi, (float)theta, (float)phi);
                }
            }
            return eulerAnglesM;
        }

        public static Vector3 EulerAnglesRadiansToEulerAnglesDegrees(Vector3 eulerAnglesRadians)
        {
            float factor=(float)(180 / Math.PI);
            return new Vector3(eulerAnglesRadians.x * factor, eulerAnglesRadians.y * factor, eulerAnglesRadians.z * factor);
        }

        public static Vector3 CrossProductRightHandRule(Vector3 a, Vector3 b)
        {
            float a1 = a.x, a2 = a.y, a3 = a.z;
            float b1 = b.x, b2 = b.y, b3 = b.z;
            Vector3 c = new Vector3(a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1);
            return c;
        }

        public static List<Vector3> SystemUToSystemM(List<Vector3> vuList)
        {
            List<Vector3> vmList = new List<Vector3>();
            for (var i = 0; i < vuList.Count; i++)
            {
                Vector3 vu = vuList[i];
                Vector3 vm = new Vector3(vu.x, vu.z, vu.y);
                vmList.Add(vm);
            }
            return vmList;
        }

        public static List<Vector3> SystemMToSystemU(List<Vector3> vmList)
        {
            List<Vector3> vuList = new List<Vector3>();
            for (var i = 0; i < vmList.Count; i++)
            {
                Vector3 vm = vmList[i];
                Vector3 vu = new Vector3(vm.x, vm.z, vm.y);
                vuList.Add(vu);
            }
            return vuList;
        }

        public static void MakeRotations(List<GameObject> gameObjectsList, List<Vector3> eulerAnglesMList)
        {
            /*
            En el sistema de coordenadas de matplotlib el orden de las rotaciones es Z, Y y X
            En el sistema de coordenadas de Unity el orden de las rotaciones debe ser Y, Z y X (para que coincida con el de matplotlib)
            */
            for(var i=0; i<gameObjectsList.Count; i++)
            {
                GameObject gameObject=gameObjectsList[i];
                Vector3 eulerAnglesM=eulerAnglesMList[i];

                // Realiza las rotaciones en el orden ZYX en el sistema matplotlib 
                // Es como igualar el sistema de Unity y el sistema de matplotlib 
                // El sistema de Unity se mueve identicamente que el sistema de matplotlib
                float psiu = eulerAnglesM.x, thetau = eulerAnglesM.y, phiu = eulerAnglesM.z;
                Quaternion rotation =
                    Quaternion.AngleAxis(-phiu, new Vector3(0, 1, 0)) *             // Rotacion en Z en matplotlib
                    Quaternion.AngleAxis(-thetau, new Vector3(0, 0, 1)) *           // Rotacion en Y en matplotlib
                    Quaternion.AngleAxis(-psiu, new Vector3(1, 0, 0));              // Rotacion en X en matplotlib
                gameObject.transform.rotation = rotation;
            }
        }

        public static void TransformsByPatternRecursiveTransform(List<Transform> transformsList, Transform rootTransform, string pattern)
        {
            // Arbol de componentes
            foreach (Transform transform in rootTransform)
            {
                if (Regex.IsMatch(transform.gameObject.name, pattern))
                {
                    transformsList.Add(transform);
                }
                if (transform.childCount > 0)
                {
                    TransformsByPatternRecursiveTransform(transformsList, transform, pattern);
                }
            }
        }

        public static void PrintTransformsList(List<Transform> transformsList)
        {
            for(var i=0; i<transformsList.Count; i++)
            {
                Debug.Log(transformsList[i].name);
            }
        }

        public static void OrderByNameTransformsList(List<Transform> transformsList)
        {
            for(var i=0; i<transformsList.Count; i++)
            {
                for(var j=i + 1; j<transformsList.Count; j++)
                {
                    if(string.Compare(transformsList[j].name, transformsList[i].name) < 0)
                    {
                        // Intercambiar valores
                        Transform temp=transformsList[j];
                        transformsList[j]=transformsList[i];
                        transformsList[i]=temp;
                    }
                }
            }
        }

        public static List<GameObject> CreateFathersWithSpecificOrientation(List<Vector4> creationCoordinateSystemList, List<Transform> jointTransformsList)
        {
            List<GameObject> jointFatherGameObjectsList=new List<GameObject>();
            // Todas las posiciones las pasamos al sistema de matplotlib
            List<Vector3> jointPositionsM=SystemUToSystemM(vuList: jointTransformsList.ConvertAll<Vector3>(obj => obj.position));
            for(var i=0; i<creationCoordinateSystemList.Count; i++)
            {
                Vector4 creationCoordinateSystem=creationCoordinateSystemList[i];
                int m=(int)creationCoordinateSystem.x, n=(int)creationCoordinateSystem.y, p=(int)creationCoordinateSystem.z, q=(int)creationCoordinateSystem.w;

                Vector3 vz_mn=jointPositionsM[n] - jointPositionsM[m];
                Vector3 v_pq=jointPositionsM[q] - jointPositionsM[p];
                Vector3 vy=CrossProductRightHandRule(a: v_pq, b: vz_mn);
                Vector3 uy=vy.normalized;
                Vector3 uz_mn=vz_mn.normalized;
                Vector3 ux=CrossProductRightHandRule(a: uy, b: uz_mn);
                List<Vector3> vmList=new List<Vector3>{ux, uy, uz_mn};
                Vector3 eulerAnglesM=EulerAnglesRadiansToEulerAnglesDegrees(eulerAnglesRadians: EulerAnglesMFromToRotationMatrix(c1: vmList[0], c2: vmList[1], c3: vmList[2]));

                GameObject jointFather = new GameObject("joint_father_" + i.ToString().PadLeft(2, '0'));
                // Rotar y posicionar el nuevo objeto padre, y hacer el enlace 
                MakeRotations(gameObjectsList: new List<GameObject>{jointFather}, eulerAnglesMList: new List<Vector3>{eulerAnglesM});
                jointFather.transform.position=jointTransformsList[i].position;
                jointFather.transform.parent=jointTransformsList[i].parent;
                jointTransformsList[i].parent=jointFather.transform;

                jointFatherGameObjectsList.Add(jointFather);
            }
            return jointFatherGameObjectsList;
        }
    }
}

namespace BytesConverter
{
    public class AlgorithmBytes
    {
        public static int bytesByStr=20;
        public static int bytesByNumber=4;
        public static List<Vector3> BytesArray3D(byte[] bytes, int numberPoints)
        {
            List<Vector3> list=new List<Vector3>();
            List<byte> bytesList=new List<byte>(bytes);
            int stepSize=bytesByNumber * 3;
            for(var i=0; i<numberPoints; i++)
            {
                List<byte> auxList=bytesList.GetRange(i * stepSize, stepSize);
                float x=BitConverter.ToSingle(auxList.GetRange(0*bytesByNumber,bytesByNumber).ToArray(),0);
                float y=BitConverter.ToSingle(auxList.GetRange(1*bytesByNumber,bytesByNumber).ToArray(),0);
                float z=BitConverter.ToSingle(auxList.GetRange(2*bytesByNumber,bytesByNumber).ToArray(),0);
                list.Add(new Vector3(x,y,z));
            }
            return list;
        }

        public static string BytesString(byte[] bytes, int n)
        {
            return Encoding.UTF8.GetString(bytes, 0, n);;
        }

        public static int BytesInt(byte[] bytes)
        {
            return BitConverter.ToInt32(bytes, 0);
        }
    }
}

namespace Algorithms
{
    public class AlgorithmMediaPipeHands
    {
        public static string algorithmName="MediaPipe Hands";
        public static int numberPoints=21;
        public static bool isDoubleEstimate=true;
        // x,y,z,w
        public static List<Vector4> creationCoordinateSystemList=new List<Vector4>{
            new Vector4(0,9,0,17),new Vector4(1,2,0,17),new Vector4(2,3,0,17),new Vector4(3,4,0,17),new Vector4(3,4,0,17),new Vector4(5,6,5,9),new Vector4(6,7,5,9),new Vector4(7,8,5,9),new Vector4(7,8,5,9),new Vector4(9,10,5,9),new Vector4(10,11,5,9),new Vector4(11,12,5,9),new Vector4(11,12,5,9),new Vector4(13,14,5,9),new Vector4(14,15,5,9),new Vector4(15,16,5,9),new Vector4(15,16,5,9),new Vector4(17,18,5,9),new Vector4(18,19,5,9),new Vector4(19,20,5,9),new Vector4(19,20,5,9)
        };
        public List<Vector3> points3DULeftList=null;
        public List<Vector3> points3DURightList=null;
        public List<Vector3> eulerAnglesMLeftList=null;
        public List<Vector3> eulerAnglesMRightList=null;

        public void SetPart(string partName, List<Vector3> points3DUList, List<Vector3> eulerAnglesMList)
        {
            if(partName == "Left")
            {
                this.points3DULeftList=points3DUList;
                this.eulerAnglesMLeftList=eulerAnglesMList;
            }
            if(partName == "Right")
            {
                this.points3DURightList=points3DUList;
                this.eulerAnglesMRightList=eulerAnglesMList;
            }
        }
    }

    public class AlgorithmMediaPipePose
    {
        public static string algorithmName="MediaPipe Pose";
        public static int numberPoints=33;
        public static bool isDoubleEstimate=false;
        // x,y,z,w
        public static List<Vector4> creationCoordinateSystemList=new List<Vector4>{
            new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(0,9,0,10),new Vector4(11,13,11,23),new Vector4(12,14,12,24),new Vector4(13,15,13,24),new Vector4(14,16,14,23),new Vector4(15,19,15,17),new Vector4(16,20,16,18),new Vector4(17,15,17,19),new Vector4(18,16,18,20),new Vector4(19,17,19,15),new Vector4(20,18,20,16),new Vector4(21,15,21,17),new Vector4(22,16,22,18),new Vector4(23,25,23,24),new Vector4(24,26,24,23),new Vector4(25,27,25,26),new Vector4(26,28,26,25),new Vector4(27,31,27,29),new Vector4(28,32,28,30),new Vector4(29,31,29,27),new Vector4(30,32,30,28),new Vector4(31,29,31,27),new Vector4(32,30,32,28)
        };
        public List<Vector3> points3DUAllList=null;
        public List<Vector3> eulerAnglesMAllList=null;

        public void SetPart(string partName, List<Vector3> points3DUList, List<Vector3> eulerAnglesMList)
        {
            if(partName == "All")
            {
                this.points3DUAllList=points3DUList;
                this.eulerAnglesMAllList=eulerAnglesMList;
            }
        }
    }
}

