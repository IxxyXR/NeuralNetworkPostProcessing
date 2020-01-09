using System.Collections;
using UnityEngine;

public class DelayedRender : MonoBehaviour
{
    public float FPS = 2f;
    private Camera renderCam;

    void Start ()
    {
        renderCam = GetComponent<Camera>();
        renderCam.enabled = false;
        InvokeRepeating (nameof(Render), 0f, 1f / FPS);
    }

    void OnDestroy(){
        //CancelInvoke ();
    }

    void Render(){
        renderCam.enabled = true;
    }

    void OnPostRender(){
        renderCam.enabled = false;
    }
}