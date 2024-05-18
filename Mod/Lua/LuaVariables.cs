using System;
using System.Collections.Generic;
using Il2CppInterop.Runtime.Injection;
using MoonSharp.Interpreter;
using SmashHammer.GearBlocks.Construction;
using SmashHammer.GearBlocks.Tweakables;
using SmashHammer.Input;
using UnityEngine;

namespace Gearthon.Lua;

class LuaVariables : Il2CppSystem.Object
{
    public LuaPart PART;
    public LuaCollider COLLIDER;
    public LuaRigidbody RIGIDBODY;
    public LuaConstruction CONSTRUCTION;
    public LuaScript SCRIPT;
    

    ScriptBehaviour script_behaviour;

    static LuaVariables()
    {
        ClassInjector.RegisterTypeInIl2Cpp<LuaVariables>();
    }

    public LuaVariables(IntPtr ptr) : base(ptr) { }
    public LuaVariables(ScriptBehaviour script_behaviour) : base(ClassInjector.DerivedConstructorPointer<LuaVariables>())
    {
        ClassInjector.DerivedConstructorBody(this);
        
        this.script_behaviour = script_behaviour;

        // COLLIDER = UserData.Create(new LuaCollider(script_behaviour.descriptor.GetComponentInChildren<Collider>()));
        PART = new LuaPart(script_behaviour.descriptor);
        CONSTRUCTION = new LuaConstruction(script_behaviour.descriptor.ParentConstruction);
        RIGIDBODY = new LuaRigidbody(script_behaviour.descriptor.parentComposite.GetComponent<Rigidbody>());
        SCRIPT = new LuaScript(script_behaviour);
        
        // Static non-updating
        script_behaviour.script.Globals.Set("Script", UserData.Create(SCRIPT));

        // Dynamic, will need to update
        script_behaviour.script.Globals.Set("Construction", UserData.Create(CONSTRUCTION));
        script_behaviour.script.Globals.Set("Rigidbody", UserData.Create(RIGIDBODY));
        script_behaviour.script.Globals.Set("Part", UserData.Create(PART));

        // Give lua access to our "helper" methods
        script_behaviour.script.Globals.Set("Debug", UserData.Create(new LuaDebug()));
        script_behaviour.script.Globals.Set("DataChannel", UserData.Create(new LuaDataChannel(script_behaviour)));
    }

    /// <summary>
    /// Internal Use Only.
    /// Updates our script with values from LuaVariables
    /// </summary>
    public void _UpdateVars()
    {
        // Update our variables
        RIGIDBODY.rigidbody.Set(script_behaviour.descriptor.parentComposite.GetComponent<Rigidbody>());
        CONSTRUCTION.construction.Set(script_behaviour.descriptor.ParentConstruction);
        PART.part.Set(script_behaviour.descriptor);
        
        foreach (KeyValuePair<string, TweakableBase> pair in script_behaviour.tweakables_dict)
        {
            if (pair.Value is IntTweakable)
                script_behaviour.script.Globals.Set(pair.Key, DynValue.FromObject(script_behaviour.script, (int)(IntTweakable)pair.Value));
            else if (pair.Value is BooleanTweakable)
                script_behaviour.script.Globals.Set(pair.Key, DynValue.FromObject(script_behaviour.script, (bool)(BooleanTweakable)pair.Value));
            else if (pair.Value is FloatTweakable)
                script_behaviour.script.Globals.Set(pair.Key, DynValue.FromObject(script_behaviour.script, (float)(FloatTweakable)pair.Value));
            else if (pair.Value is StringTweakable)
                script_behaviour.script.Globals.Set(pair.Key, DynValue.FromObject(script_behaviour.script, (string)(StringTweakable)pair.Value));
            // else if (pair.Value is JoystickAxisTweakable)
            //     script_behaviour.script.Globals.Set(pair.Key, DynValue.FromObject(script_behaviour.script, (int)(IntTweakable)pair.Value));
            else if (pair.Value is InputActionTweakable)
                script_behaviour.script.Globals.Set(pair.Key, DynValue.FromObject(script_behaviour.script, new LuaInputAction((InputAction)(InputActionTweakable)pair.Value)));
        }
    }
}