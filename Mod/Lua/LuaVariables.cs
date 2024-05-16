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
    public bool ACTIVE;
    public LuaPart PART;
    public LuaCollider COLLIDER;
    public LuaRigidbody RIGIDBODY;
    public LuaConstruction CONSTRUCTION;
    

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
                
        // Give lua access to our types
        // script_behaviour.script.Globals.Set("Collider", UserData.Create(new LuaCollider(COLLIDER)));
        
        PART = new LuaPart(script_behaviour.descriptor);
        ACTIVE = script_behaviour.IsActivated;
        // COLLIDER = UserData.Create(new LuaCollider(script_behaviour.descriptor.GetComponentInChildren<Collider>()));
        CONSTRUCTION = new LuaConstruction(script_behaviour.descriptor.ParentConstruction);
        RIGIDBODY = new LuaRigidbody(script_behaviour.descriptor.parentComposite.GetComponent<Rigidbody>());

        // Give lua access to our "helper" methods
        script_behaviour.script.Globals.Set("Debug", UserData.Create(new LuaDebug()));
        script_behaviour.script.Globals.Set("DataChannel", UserData.Create(new LuaDataChannel(script_behaviour)));

        _UpdateVars();
    }

    /// <summary>
    /// Internal Use Only.
    /// Updates our script with values from LuaVariables
    /// </summary>
    public void _UpdateVars()
    {
        // Update our variables
        ACTIVE = script_behaviour.IsActivated;
        CONSTRUCTION.construction.Set(script_behaviour.descriptor.ParentConstruction);
        RIGIDBODY.rigidbody.Set(script_behaviour.descriptor.parentComposite.GetComponent<Rigidbody>());
        PART.part.Set(script_behaviour.descriptor);

        script_behaviour.script.Globals.Set("Active", DynValue.NewBoolean(ACTIVE));
        script_behaviour.script.Globals.Set("Construction", UserData.Create(CONSTRUCTION));
        script_behaviour.script.Globals.Set("Rigidbody", UserData.Create(RIGIDBODY));
        script_behaviour.script.Globals.Set("Part", UserData.Create(PART));
        
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