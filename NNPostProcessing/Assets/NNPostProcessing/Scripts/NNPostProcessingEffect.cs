// neural network post-processing

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

namespace NNPP
{

    [System.Serializable]
    [RequireComponent(typeof(Camera))]
    public class NNPostProcessingEffect : MonoBehaviour
    {
        public int RenderEvery = 20;
        private RenderTexture renderedFrame;

        public NNStyle style = NNStyle.starry_night;

        private NNModel model;

        void Start()
        {
            model = new NNModel();
            model.Load(style.ToString());
        }

        void OnDisable()
        {
            model.Release();
        }

        void OnRenderImage(RenderTexture src, RenderTexture dst)
        {
            if (Time.frameCount % RenderEvery == 0)
            {
                renderedFrame = model.Predict(src);
            }
            Graphics.Blit(renderedFrame, dst);
        }

    }

    public enum NNStyle
    {
        des_glaneuses,
        la_muse,
        mirror,
        sketch,
        starry_night,
        udnie,
        wave
    }
}