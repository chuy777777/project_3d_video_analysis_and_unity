using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class SocketMessageCanvas : MonoBehaviour
{
    public static SocketMessageCanvas instance;
    public TMP_Text message;

    void Awake()
    {
        if(SocketMessageCanvas.instance == null){
            SocketMessageCanvas.instance=this;
        }else{
            Destroy(this.gameObject);
        }
    }

    void Start()
    {
        this.message=this.transform.Find("Background").Find("Message").GetComponent<TMP_Text>();
    }

    void Update()
    {
        
    }
}
