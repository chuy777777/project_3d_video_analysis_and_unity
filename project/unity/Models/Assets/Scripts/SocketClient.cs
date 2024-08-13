using System;
using System.Text; 
using System.Net; 
using System.Net.Sockets; 
using System.Threading; 
using System.Threading.Tasks;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

using MyNamespace;
using Algorithms;
using BytesConverter;

public class SocketClient : MonoBehaviour
{
    public static SocketClient instance;
    private TMP_InputField inputHost, inputPort;
    private Socket client=null;
    private IPEndPoint ipEndPoint;
    private Thread thread;
    public AlgorithmMediaPipeHands algorithmMediaPipeHands=new Algorithms.AlgorithmMediaPipeHands();
    public AlgorithmMediaPipePose algorithmMediaPipePose=new Algorithms.AlgorithmMediaPipePose();

    public void Awake()
    {
        if(SocketClient.instance == null)
        {
            SocketClient.instance=this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        this.inputHost=GameObject.Find("Host").GetComponent<TMP_InputField>();
        this.inputPort=GameObject.Find("Port").GetComponent<TMP_InputField>();
    }

    public void OnApplicationQuit(){
        this.CloseConnection();
    }

    public void CloseConnection()
    {
        if (this.client != null)
        {
            try
            {
                /*
                    - SocketShutdown.Send       --> Deshabilitar el envío en este socket 
                    - SocketShutdown.Receive    --> Deshabilitar la recepción en este socket   
                    - SocketShutdown.Both       --> Deshabilitar tanto el envío como la recepción en este socket 
                */
                this.client.Shutdown(SocketShutdown.Both);
                this.client.Close();
                SocketMessageCanvas.instance.message.text="Conexion cerrada exitosamente";
            }
            catch (ThreadAbortException e) 
            {
                SocketMessageCanvas.instance.message.text="(ThreadAbortException): "+e.Message;
            }
            catch (SocketException e)
            {
                SocketMessageCanvas.instance.message.text="(SocketException): "+e.Message;
            }
            catch (UnityException e)
            {
                SocketMessageCanvas.instance.message.text="(UnityException): "+e.Message;
            }
            catch (Exception e) 
            {
                SocketMessageCanvas.instance.message.text="(Exception): "+e.Message;
            }
            finally
            {
                this.client=null;
            }
        }
    } 

    public void StartClient()
    {
        if(this.client == null){
            try
            {
                this.client=this.GetSocket();
                this.client.Connect(this.ipEndPoint);
                this.StartThread();
                SocketMessageCanvas.instance.message.text="Se ha establecido una conexion con el servidor";
            }
            catch (ThreadAbortException e) 
            {
                this.CloseConnection();
                SocketMessageCanvas.instance.message.text="(ThreadAbortException): "+e.Message;
            }
            catch (SocketException e)
            {
                this.CloseConnection();
                SocketMessageCanvas.instance.message.text="(SocketException): "+e.Message;
            }
            catch (UnityException e)
            {
                this.CloseConnection();
                SocketMessageCanvas.instance.message.text="(UnityException): "+e.Message;
            }
            catch (Exception e) 
            {
                this.CloseConnection();
                SocketMessageCanvas.instance.message.text="(Exception): "+e.Message;
            }
        }
    }

    public Socket GetSocket()
    {
        string host=this.inputHost.text;
        int port;

        try
        {
            port=Int32.Parse(this.inputPort.text);
        }
        catch (FormatException){
        {
            port=5000;
            this.inputPort.text=port.ToString();
        }}

        IPAddress ipAddress=IPAddress.Parse(host);
        this.ipEndPoint=new IPEndPoint(ipAddress, port);
        return new Socket(
            this.ipEndPoint.AddressFamily, 
            SocketType.Stream, 
            ProtocolType.Tcp
        );
    }

    public void StartThread()
    {
        this.thread=new Thread(new ThreadStart(this.ClientFunction)); 		
        this.thread.IsBackground = true; 		
        this.thread.Start();
    }

    /*
    En esta funcion no se pueden llamar a clases de Unity 
    (solo es posible en el hilo principal)
    */
    public void ClientFunction()
    {
        try
        {
            while(true)
            {
                // Enviar datos
                int data=1;
                byte[] bytes=BitConverter.GetBytes(data);
                this.client.Send(bytes);

                // Recibir datos
                int bytesByStr=BytesConverter.AlgorithmBytes.bytesByStr;
                int bytesByNumber=BytesConverter.AlgorithmBytes.bytesByNumber;
                
                byte[] bytesExistsData=new byte[bytesByNumber];
                int receivedExistsData=client.Receive(bytesExistsData);
                if(receivedExistsData == 0) break;
                int existsData=BytesConverter.AlgorithmBytes.BytesInt(bytes: bytesExistsData);

                if(existsData == 1)
                {
                    byte[] bytesNumberAlgorithms=new byte[bytesByNumber];
                    int receivedNumberAlgorithms=client.Receive(bytesNumberAlgorithms);
                    if(receivedNumberAlgorithms == 0) break;
                    int numberAlgorithms=BytesConverter.AlgorithmBytes.BytesInt(bytes: bytesNumberAlgorithms);

                    bool isOk=false;
                    for(var i=0; i<numberAlgorithms; i++)
                    {
                        byte[] bytesAlgorithmName=new byte[bytesByStr];
                        int receivedAlgorithmName=client.Receive(bytesAlgorithmName);
                        if(receivedAlgorithmName == 0) break;
                        string algorithmName=BytesConverter.AlgorithmBytes.BytesString(bytes: bytesAlgorithmName, n: receivedAlgorithmName);
                        algorithmName=algorithmName.Trim();

                        byte[] bytesNumberPoints=new byte[bytesByNumber];
                        int receivedNumberPoints=client.Receive(bytesNumberPoints);
                        if(receivedNumberPoints == 0) break;
                        int numberPoints=BytesConverter.AlgorithmBytes.BytesInt(bytes: bytesNumberPoints);

                        byte[] bytesNumberParts=new byte[bytesByNumber];
                        int receivedNumberParts=client.Receive(bytesNumberParts);
                        if(receivedNumberParts == 0) break;
                        int numberParts=BytesConverter.AlgorithmBytes.BytesInt(bytes: bytesNumberParts);

                        bool isOk2=false;
                        for(var j=0; j<numberParts; j++)
                        {
                            byte[] bytesPartName=new byte[bytesByStr];
                            int receivedPartName=client.Receive(bytesPartName);
                            if(receivedPartName == 0) break;
                            string partName=BytesConverter.AlgorithmBytes.BytesString(bytes: bytesPartName, n: receivedPartName);
                            partName=partName.Trim();

                            byte[] bytesPoints3DU=new byte[numberPoints * 3 * bytesByNumber];
                            int receivedPoints3DU=client.Receive(bytesPoints3DU);
                            if(receivedPoints3DU == 0) break;
                            List<Vector3> points3DUList=BytesConverter.AlgorithmBytes.BytesArray3D(bytes: bytesPoints3DU, numberPoints: numberPoints);

                            byte[] bytesEulerAnglesM=new byte[numberPoints * 3 * bytesByNumber];
                            int receivedEulerAnglesM=client.Receive(bytesEulerAnglesM);
                            if(receivedEulerAnglesM == 0) break;
                            List<Vector3> eulerAnglesMList=BytesConverter.AlgorithmBytes.BytesArray3D(bytes: bytesEulerAnglesM, numberPoints: numberPoints);
                            
                            if(algorithmName == Algorithms.AlgorithmMediaPipeHands.algorithmName)
                            {
                                this.algorithmMediaPipeHands.SetPart(partName: partName, points3DUList: points3DUList, eulerAnglesMList: eulerAnglesMList);
                            }
                            if(algorithmName == Algorithms.AlgorithmMediaPipePose.algorithmName)
                            {
                                this.algorithmMediaPipePose.SetPart(partName: partName, points3DUList: points3DUList, eulerAnglesMList: eulerAnglesMList);
                            }
                            if(j == numberParts - 1) isOk2=true;
                        }
                        if(!isOk2) break;
                        if(i == numberAlgorithms - 1) isOk=true;
                    }
                    if(!isOk) break;
                }
            }
            // El servidor se ha desconectado
            this.client.Shutdown(SocketShutdown.Both);
            this.client.Close();
            this.client=null;
        }
        catch (ThreadAbortException) {}
        catch (SocketException) {}
        catch (UnityException) {}
        catch (Exception) {}
    }
}
