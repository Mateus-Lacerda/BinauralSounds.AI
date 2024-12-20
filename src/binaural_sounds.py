from utils.colors import Colors as cl
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description=cl.colored("""\
BinauralSounds.AI
----------------------------------
This app is a collection of tools to generate binaural sounds.
    1. Load the pretrained model facebook/audiogen-medium
    2. Serve the model API locally with ngrok
        2.1. This will trigger a notification with the ngrok URL to the main app.
    3. Serve the feedback app locally with Streamlit
    4. Run the app locally
    5. If it's working, deploy the app to your favorite cloud provider.
----------------------------------\
                                     """, "GREEN"), 
                                     epilog=cl.colored("""\
----------------------------------
Have fun!\
                                                       """, "BLUE"))
    parser.add_argument("-lm", "--load_model", action="store_true", help="Load the pretrained model facebook/audiogen-medium")
    parser.add_argument("-sm", "--serve_model", action="store_true", help="Serve the model API locally with ngrok")
    parser.add_argument("-g", "--generate", action="store_true", help="Activate the music generation")
    parser.add_argument("-sa", "--serve_app", action="store_true", help="Serve the feedback app locally with Streamlit")
    parser.add_argument("-b", "--binauralize", action="store_true", help="Binauralize a sound from the `audioinput` folder")
    parser.add_argument("-bi", "--binauralize_input", type=str, help="The input file to binauralize")
    parser.add_argument("-bf", "--binauralize_frequency", type=int, help="The frequency difference between the two channels")
    args = parser.parse_args()

    if args.load_model:
        from audio_model.load_model import load_model
        load_model()
    if args.serve_model:
        if args.generate:
            import os
            from audio_model.cuda_test import test_cuda
            test_cuda()
            os.environ["ENV"] = "gen-on"
        from model_api.model_api import run
        run()
    if args.serve_app:
        import sys
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", "src/feedback_app/feedback_app.py"]
        sys.exit(stcli.main())

    if args.binauralize:
        import os
        import sys
        from binauralize import binauralize
        if not args.binauralize_input or not args.binauralize_frequency:
            print(cl.colored("You need to provide the input file and the frequency difference between the two channels.", "RED"))
        else:
            if not os.path.exists("audioinput"):
                os.mkdir("audioinput")
            if not os.path.exists("audiooutput"):
                os.mkdir("audiooutput")
            if not any(os.listdir("audioinput")) or not os.path.exists(f"audioinput/{args.binauralize_input}"):
                print(cl.colored("The input file does not exist.", "RED"))
                sys.exit(1)
            if not "." in args.binauralize_input:
                print(cl.colored("The input file must have an extension.", "RED"))
                sys.exit(1)
            
            binauralize(f"audioinput/{args.binauralize_input}", args.binauralize_frequency)
        
    if not any(vars(args).values()):
        parser.print_help()
    